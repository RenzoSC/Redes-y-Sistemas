
#ifndef TRANSPORTTX
#define TRANSPORTTX

#include <string.h>
#include <omnetpp.h>
#include "FeedPacket_m.h"

using namespace omnetpp;

class TransportTx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    int packet_lost;
    int packet_slot;
    bool controlPkt_send;

    bool firstControlSend;

    void sendControlPacket();
public:
    TransportTx();
    virtual ~TransportTx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportTx);

TransportTx::TransportTx() {
    endServiceEvent = NULL;
}

TransportTx::~TransportTx() {
    cancelAndDelete(endServiceEvent);
}

void TransportTx::sendControlPacket(){
    controlPkt_send = true;
    //creamos un paquete de feedback
    FeedPacket* feedbackPkt = new FeedPacket();
    feedbackPkt->setByteLength(20);
    feedbackPkt->setKind(2);

    //indicamos en el campo remainingBuffer cuanto espacio queda del buffer
    int remain = par("bufferSize").intValue();
    feedbackPkt->setRemainingBuffer(remain);

    //lo enviamos por el canal correspondiente
    send(feedbackPkt, "toOut$o");
}

void TransportTx::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    packet_lost = 0;
    packet_slot = 0;
    controlPkt_send = false;
    bufferSizeVector.setName("Buffer Size");
    packetDropVector.setName("Total packet loss");

    firstControlSend = false;

}

void TransportTx::finish() {
}

void TransportTx::handleMessage(cMessage *msg) {
    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            if(this->packet_slot-- > 0){
                // dequeue packet
                cPacket *pkt = (cPacket*) buffer.pop();
                // send packet
                send(pkt, "toOut$o");
                // start new service
                serviceTime = pkt->getDuration();
                scheduleAt(simTime() + serviceTime, endServiceEvent);
            }else if(this->packet_slot <= 0 && !this->controlPkt_send){sendControlPacket();}
        }
    } else {
        if(!firstControlSend){
            firstControlSend = true;
            //first Feedback Pkt   (similar to connect with the other node)
            sendControlPacket();
        }

      //if msg is a packet
        if(msg->getKind() == 2) {
        //if msg is a feedback packet
            FeedPacket* feedbackPkt = (FeedPacket*)msg;

            int remainingBuffer = feedbackPkt->getRemainingBuffer();
            this->packet_slot = remainingBuffer;
            this->controlPkt_send = false;

            // if the server is idle
            if (!endServiceEvent->isScheduled()) {
                // start the service
                scheduleAt(simTime(), endServiceEvent);
            }

            delete msg;    //eliminamos el feedpacket que se recibió
            //Aca lo que se hace con el pkt
        }else if (msg->getKind() == 0) {
        //if msg is a data packet
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

#endif /* TRANSPORTTX */
