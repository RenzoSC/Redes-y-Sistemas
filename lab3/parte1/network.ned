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

module NodeTx
{
    parameters:
        @display("i=block/routing");
    gates:
        output out;
    submodules:
        gen: Generator {
            @display("p=75,50");
        }
        queue: Queue {
            @display("p=75,190");
        }
    connections:
        gen.out --> queue.in;
        queue.out --> out;

}

module NodeRx
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
    submodules:
        sink: Sink {
            @display("p=75,50");
        }
        queue: Queue {
            @display("p=75,190");
        }
    connections:
        in --> queue.in;
        //case study 1:
        //queue.out --> {  datarate = 0.5 Mbps; } --> sink.in;
        //case study 2:
        queue.out --> {  datarate = 1 Mbps; } --> sink.in;
                
}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,30");
        }
        queue: Queue {
            @display("p=130,30");
        }
        nodeRx: NodeRx {
            @display("p=230,30");
        }
    connections:
        nodeTx.out --> {  datarate = 1 Mbps; delay = 100 us; } --> queue.in;
        //case study 1:
        //queue.out --> { datarate = 1 Mbps; delay = 100 us; } --> nodeRx.in;
        //case study 2:
        queue.out --> {  datarate = 0.5 Mbps; delay = 100 us; } --> nodeRx.in;
}
