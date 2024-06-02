#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include <hello_m.h>
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef vector<ll> vl;
ll INF = 1e18;

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    vector<vector<pair<int,int>>>graphNetwork;
    int nodeName;
    int numGates;
    vector<int>whereToSend;
    cMessage * sayHi;
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    virtual bool isSayHiMsg(cMessage * msg);
    void bfs(ll v, vector<vl> &g, vector<bool> &vis, vector<ll> &dis);

    virtual void sayHiToNeighbours();
    virtual bool isHelloPkt(Packet * pkt);
    virtual void actualizeInformation(Hello *pkt);
    virtual void processInformation(Hello *pkt);

    //functions to debug
    virtual void printGateInformation(Hello *pkt);
    virtual void printNeighInformation(Hello *pkt);
    virtual void printGraphInformation(Hello *pkt);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::bfs(ll v, vector<vl> &g, vector<bool> &vis, vector<ll> &dis) {
    queue<ll> q;
    vis[v] = true;
    q.push(v);
    while (!q.empty()) {
        v = q.front();
        q.pop();
        for (ll u : g[v]) {
            if (!vis[u]) {
                vis[u] = true;
                q.push(u);
                dis[u] = dis[v]+1;
            }
        }
    }
}


void Net::initialize() {
    nodeName = this->getParentModule()->getIndex();
    sayHi = new cMessage("Say Hi");
    scheduleAt(simTime(), sayHi);
}

void Net::finish() {
}

void Net::sayHiToNeighbours(){
    Hello *pkt = new Hello();
    pkt->setGateIndexFrom(1);
    pkt->setDestination(-1);
    pkt->setHopCount(0);
    pkt->setSource(nodeName);
    pkt->setOriginalSource(nodeName);
    send(pkt,"toLnk$o",1);
}

bool Net::isSayHiMsg(cMessage * msg){
    return msg == sayHi;
}

bool Net::isHelloPkt(Packet * pkt){
    return pkt->getDestination()==-1;
}

void Net::actualizeInformation(Hello * pkt){
    int gateFrom = pkt->getGateIndexFrom();
    int count = pkt->getHopCount();
    int fromNode = pkt->getSource();
    pkt->setGateIndexArraySize((count+1)*2);
    pkt->setNeighboursArraySize((count+1)*2);
    pkt->setGateIndex(count*2, gateFrom);
    pkt->setNeighbours(count*2, nodeName);
    pkt->setGateIndex((count*2)+1, pkt->getArrivalGate()->getIndex());
    pkt->setNeighbours((count*2)+1,fromNode);
    pkt->setSource(nodeName);
    pkt->setHopCount(count+1);
}

void Net::processInformation(Hello *pkt){
    int lados = pkt->getHopCount();
    graphNetwork.resize(lados);
    whereToSend.resize(lados);
    for (size_t i = 0; i < lados; i++)
    {
        int y = pkt->getNeighbours(i*2);
        int gateToY = pkt->getGateIndex(i*2);
        int x = pkt->getNeighbours(i*2+1);
        int gateToX = pkt->getGateIndex((i*2+1));
        graphNetwork[x].push_back({y,gateToY});
        graphNetwork[y].push_back({x,gateToX});
        whereToSend[i]=-1;                       //<-- inicializo a donde enviar en -1 (ningun gate es -1)
    }
}

void Net::printNeighInformation(Hello *hpkt){
    for (size_t i = 0; i < hpkt->getNeighboursArraySize(); i++)
    {
        std::cout<<hpkt->getNeighbours(i)<<" ";
    }
    std::cout<<"\n";
}

void Net::printGateInformation(Hello *hpkt){
    for (size_t i = 0; i < hpkt->getGateIndexArraySize(); i++)
    {
        std::cout<<hpkt->getGateIndex(i)<<" ";
    }
    std::cout<<"\n";
}

void Net::printGraphInformation(Hello *pkt){
    for (size_t i = 0; i < graphNetwork.size(); i++)
    {
        std::cout<<i<<" :[";
        for (size_t j = 0; j < graphNetwork[i].size(); j++)
        {
            std::cout<<"{"<<graphNetwork[i][j].first<<" , "<<graphNetwork[i][j].second<<"}, ";
        }
        std::cout<<"]"<<"\n";
    }
}


void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;
    Hello * hpkt = (Hello *)msg;
    int actual_node = this->getParentModule()->getIndex();
    int dest_node = pkt->getDestination();
    
    if(isSayHiMsg(msg)){
        //empieza a decirle hello a su vecino
        sayHiToNeighbours();
    }else if(isHelloPkt(pkt)){
        //caso en el que el hello llegó a otro nodo distinto del original de donde se envió
        if (hpkt->getOriginalSource() != nodeName){
            actualizeInformation(hpkt);
            send(pkt,"toLnk$o",hpkt->getGateIndexFrom());   //lo vuelvo a enviar en el mismo sentido
        } else {
            //caso en el que el hello llegó al nodo original desde donde se envió
            //actualizar info
            actualizeInformation(hpkt);

            //processInformation(hpkt);   //descomentar
            if(nodeName == 0){   //usado solo para debugear xd  --> dsp borrar
                printNeighInformation(hpkt);
                printGateInformation(hpkt);
                processInformation(hpkt);
                printGateInformation(hpkt);
            }
            //de acá no hay que hacer más nada
            delete(msg);
        }
    }else{
        // If this node is the final destination, send to App
        if ( dest_node == actual_node) {
            send(msg, "toApp$o");
        }
        // If not, forward the packet to some else... to who?
        else {
            // We send to link interface #0, which is the
            // one connected to the clockwise side of the ring
            // Is this the best choice? are there others?
            send(msg, "toLnk$o",0);


            //acá lo que hay que hacer es como ya tenemos el grafo completo
            //hacer un algoritmo en el cual calcule por donde (por qué gate) tengo que enviar
            //el paquete para llegar a x nodo

            //lo que se podría hacer es bfs y reconstruir el camino al nodo
            //ver cual fue la primera compuerta que se utilizó y listo
            
            //como tenemos ya inicializado el whereToSend todos en -1
            //primero antes de hacer bfs deveriamos hacer
            //whereToSend[toNode] !=-1? si da true entonces enviamos por donde indica el whereToSend
            //si da false entonces hacemos el calculo de bfs, reconstruimos el camino y actualizamos el
            //whereToSend[toNode] al valor del primer gate que usamos
            //incluso no solo podríamos cambiar el valor del toNode, como podemos asumir q es un anillo
            //si el camino de X a Y es el mas corto, también lo será para todo M que se encuentre entre X e Y
            //entonces podemos actualizar esos valores también
        }
    }
}
