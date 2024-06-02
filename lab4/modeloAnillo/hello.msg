import packet;

packet Hello extends Packet {
    int gateIndexFrom;
    int gateIndex[];
    int neighbours[];
    int neighName;
    int countRound;
    int originalSource;
}