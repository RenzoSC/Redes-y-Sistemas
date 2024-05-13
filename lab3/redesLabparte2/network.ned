simple Generator
{
    parameters:
        volatile double generationInterval; // sec
        volatile int packetByteSize;  //tamaño de paquete en bytes
        @display("i=block/source");
    gates:
        output out;
}

simple Sink
{
    parameters:
        @display("i=block/sink");
    gates:
        input in;
}

simple Queue
{
    parameters:
        //volatile double serviceTime; // sec
        volatile int bufferSize;  //tamaño de buffer
        @display("i=block/queue;q=buffer");
    gates:
        input in;
        output out;
}

simple TransportTx
{
    parameters:
        int bufferSize;  //tamaño de buffer
        @display("i=block/queue;q=buffer");
    gates:
        input toApp;
        inout toOut;
}

simple TransportRx
{
    parameters:
        int bufferSize;  //tamaño de buffer
        @display("i=block/queue;q=buffer");
    gates:
        output toApp;
        inout toOut;
}

module NodeTx
{
    parameters:
        @display("i=block/routing");
    gates:
        output out;
        input in;
    submodules:
        gen: Generator {
            @display("p=40,45");
        }
        traTx: TransportTx {
            @display("p=140,45");
        }
    connections:
        gen.out --> traTx.toApp;
        traTx.toOut$o --> out;
        
        //Feedback
        in --> traTx.toOut$i;

}

module NodeRx
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
        output out;
    submodules:
        sink: Sink {
            @display("p=145,45");
        }
        traRx: TransportRx {
            @display("p=45,45");
        }
    connections:
        in --> traRx.toOut$i;
        //case study 1:
        //traRx.toApp --> {  datarate = 0.5 Mbps; } --> sink.in;
        //case study 2:
        traRx.toApp --> {  datarate = 1 Mbps; } --> sink.in;
        
        //Feedback
        traRx.toOut$o --> out;

}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,40");
        }
        dataQueue: Queue {
            @display("p=130,40");
        }
        feedbackQueue: Queue {
            @display("p=130,100");
        }
        nodeRx: NodeRx {
            @display("p=230,40");
        }
    connections:
        nodeTx.out --> {  datarate = 1 Mbps; delay = 100 us; } --> dataQueue.in;
        //case study 1:
        //dataQueue.out --> {  datarate = 1 Mbps; delay = 100 us; } --> nodeRx.in;
        //case study 2:
        dataQueue.out --> {  datarate = 0.5 Mbps; delay = 100 us; } --> nodeRx.in;
        
        //FeedBack
        nodeRx.out --> feedbackQueue.in;
        feedbackQueue.out --> nodeTx.in;
}