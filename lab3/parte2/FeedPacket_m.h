//
// Generated file, do not edit! Created by opp_msgtool 6.0 from FeedPacket.msg.
//

#ifndef __FEEDPACKET_M_H
#define __FEEDPACKET_M_H

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wreserved-id-macro"
#endif
#include <omnetpp.h>

// opp_msgtool version check
#define MSGC_VERSION 0x0600
#if (MSGC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of opp_msgtool: 'make clean' should help.
#endif

class FeedPacket;
/**
 * Class generated from <tt>FeedPacket.msg:1</tt> by opp_msgtool.
 * <pre>
 * packet FeedPacket
 * {
 *     int remainingBuffer;
 * }
 * </pre>
 */
class FeedPacket : public ::omnetpp::cPacket
{
  protected:
    int remainingBuffer = 0;

  private:
    void copy(const FeedPacket& other);

  protected:
    bool operator==(const FeedPacket&) = delete;

  public:
    FeedPacket(const char *name=nullptr, short kind=0);
    FeedPacket(const FeedPacket& other);
    virtual ~FeedPacket();
    FeedPacket& operator=(const FeedPacket& other);
    virtual FeedPacket *dup() const override {return new FeedPacket(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const override;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b) override;

    virtual int getRemainingBuffer() const;
    virtual void setRemainingBuffer(int remainingBuffer);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const FeedPacket& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, FeedPacket& obj) {obj.parsimUnpack(b);}


namespace omnetpp {

template<> inline FeedPacket *fromAnyPtr(any_ptr ptr) { return check_and_cast<FeedPacket*>(ptr.get<cObject>()); }

}  // namespace omnetpp

#endif // ifndef __FEEDPACKET_M_H

