/*
 * Queue.cc
 *
 *  Created on: 4 may. 2024
 *      Author: renzo
 */

#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>
#include "FeedPacket_m.h"

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    int packet_lost;
    bool controlPkt;
    int ctrlPktPos;
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    packet_lost = 0;
    controlPkt = false;
    ctrlPktPos = 0;
    bufferSizeVector.setName("Buffer Size");
    packetDropVector.setName("Total packet loss");
}

void Queue::finish() {
}

void Queue::handleMessage(cMessage *msg) {

    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            if(this->controlPkt && this->ctrlPktPos-- == 1){
                FeedPacket *pkt = (FeedPacket*) buffer.pop();
                //hago -1 por si el buffer tiene tamaño 200
                //se guarden solo 199 data pkts para que siempre pueda entrar el control pkt
                int localbuffer = par("bufferSize").intValue()-1;
                int remainingBuffer = fmin(pkt->getRemainingBuffer(),localbuffer);
                pkt->setRemainingBuffer(remainingBuffer);
                this->controlPkt = false;
                // send packet
                send(pkt, "out");
                // start new service
                serviceTime = pkt->getDuration();
                scheduleAt(simTime() + serviceTime, endServiceEvent);
            }
            else{
                cPacket *pkt = (cPacket*) buffer.pop();
                // send packet
                send(pkt, "out");
                // start new service
                serviceTime = pkt->getDuration();
                scheduleAt(simTime() + serviceTime, endServiceEvent);
            }
        }
    } else {
        if(msg->getKind() == 2){
            //Modificar remainingBuffer y Reenviar
            FeedPacket* feedbackPkt = (FeedPacket*)msg;

            
            this->controlPkt = true;

            // enqueue the packet
            buffer.insert(feedbackPkt);
            this->ctrlPktPos = buffer.getLength();
            bufferSizeVector.record(this->ctrlPktPos);
            this->bubble("Feedback");
            // if the server is idle
            if (!endServiceEvent->isScheduled()) {
                // start the service
                scheduleAt(simTime(), endServiceEvent);
            }
        }else if (msg->getKind() == 0) {
            // if msg is a data packet
            //check buffer limit
            if(buffer.getLength() >= par("bufferSize").intValue()){
                //drop the packet
                delete msg;
                this->bubble("Packet Dropped");
                this->packet_lost +=1;
                packetDropVector.record(this->packet_lost);
            }else{
                // enqueue the packet
                buffer.insert(msg);
                bufferSizeVector.record(buffer.getLength());
                this->bubble("Encolado");
                // if the server is idle
                if (!endServiceEvent->isScheduled()) {
                    // start the service
                    scheduleAt(simTime(), endServiceEvent);
                }
            }
        }
    }
}

#endif /* QUEUE */
