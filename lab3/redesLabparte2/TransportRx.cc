
#ifndef TRANSPORTRX
#define TRANSPORTRX

#include <string.h>
#include <omnetpp.h>
#include "FeedPacket_m.h"

using namespace omnetpp;

class TransportRx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    cOutVector remainBufferVector;
    int packet_lost;

    void addPacketToBuffer(cMessage * msg);
    bool isEmptyBuffer();
    bool isFullBuffer();
    void sendDataPacket();
    void turnOnData();

    void scheduleEventWithDelay(simtime_t delay, cMessage * event);
public:
    TransportRx();
    virtual ~TransportRx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportRx);

TransportRx::TransportRx() {
    endServiceEvent = NULL;
}

TransportRx::~TransportRx() {
    cancelAndDelete(endServiceEvent);
}

void TransportRx::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    packet_lost = 0;
    bufferSizeVector.setName("Buffer Size");
    packetDropVector.setName("Total packet loss");
    remainBufferVector.setName("Remain Buffer");
}

void TransportRx::finish() {
}

bool TransportRx::isEmptyBuffer(){
    return buffer.isEmpty();
}

bool TransportRx::isFullBuffer(){
    return buffer.getLength() >= par("bufferSize").intValue();
}

void TransportRx::turnOnData(){
    // if the server is idle
    if (!endServiceEvent->isScheduled()) {
        scheduleEventWithDelay(0,endServiceEvent);
    }
}

void TransportRx::addPacketToBuffer(cMessage * msg){
    //check buffer limit
    if(isFullBuffer()){
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
        turnOnData();
    }
}

void TransportRx::sendDataPacket(){
    if(!isEmptyBuffer()){
        // dequeue packet
        cPacket *pkt = (cPacket*) buffer.pop();

        // send packet
        send(pkt, "toApp");

        //start new service
        scheduleEventWithDelay(pkt->getDuration(), endServiceEvent);
    }
    
}

void TransportRx::scheduleEventWithDelay(simtime_t delay, cMessage * event){
    scheduleAt(simTime() + delay, event);
}

void TransportRx::handleMessage(cMessage *msg) {

    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!isEmptyBuffer()) {
            sendDataPacket();
        }
    } else {
        if(msg->getKind() == 2){
            //Modificar remainingBuffer y Reenviar
            FeedPacket* feedbackPkt = (FeedPacket*)msg;

            int localbuffer = par("bufferSize").intValue() - buffer.getLength();
            int remainingBuffer = fmin(feedbackPkt->getRemainingBuffer(),localbuffer);
            feedbackPkt->setRemainingBuffer(remainingBuffer);

            send(feedbackPkt, "toOut$o");
        }else if (msg->getKind() == 0) {
            // if msg is a data packet
            addPacketToBuffer(msg);
        }
    }
}

#endif /* TRANSPORTRX */
