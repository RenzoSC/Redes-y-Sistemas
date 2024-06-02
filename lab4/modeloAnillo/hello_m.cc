//
// Generated file, do not edit! Created by opp_msgtool 6.0 from hello.msg.
//

// Disable warnings about unused variables, empty switch stmts, etc:
#ifdef _MSC_VER
#  pragma warning(disable:4101)
#  pragma warning(disable:4065)
#endif

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wshadow"
#  pragma clang diagnostic ignored "-Wconversion"
#  pragma clang diagnostic ignored "-Wunused-parameter"
#  pragma clang diagnostic ignored "-Wc++98-compat"
#  pragma clang diagnostic ignored "-Wunreachable-code-break"
#  pragma clang diagnostic ignored "-Wold-style-cast"
#elif defined(__GNUC__)
#  pragma GCC diagnostic ignored "-Wshadow"
#  pragma GCC diagnostic ignored "-Wconversion"
#  pragma GCC diagnostic ignored "-Wunused-parameter"
#  pragma GCC diagnostic ignored "-Wold-style-cast"
#  pragma GCC diagnostic ignored "-Wsuggest-attribute=noreturn"
#  pragma GCC diagnostic ignored "-Wfloat-conversion"
#endif

#include <iostream>
#include <sstream>
#include <memory>
#include <type_traits>
#include "hello_m.h"

namespace omnetpp {

// Template pack/unpack rules. They are declared *after* a1l type-specific pack functions for multiple reasons.
// They are in the omnetpp namespace, to allow them to be found by argument-dependent lookup via the cCommBuffer argument

// Packing/unpacking an std::vector
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::vector<T,A>& v)
{
    int n = v.size();
    doParsimPacking(buffer, n);
    for (int i = 0; i < n; i++)
        doParsimPacking(buffer, v[i]);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::vector<T,A>& v)
{
    int n;
    doParsimUnpacking(buffer, n);
    v.resize(n);
    for (int i = 0; i < n; i++)
        doParsimUnpacking(buffer, v[i]);
}

// Packing/unpacking an std::list
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::list<T,A>& l)
{
    doParsimPacking(buffer, (int)l.size());
    for (typename std::list<T,A>::const_iterator it = l.begin(); it != l.end(); ++it)
        doParsimPacking(buffer, (T&)*it);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::list<T,A>& l)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        l.push_back(T());
        doParsimUnpacking(buffer, l.back());
    }
}

// Packing/unpacking an std::set
template<typename T, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::set<T,Tr,A>& s)
{
    doParsimPacking(buffer, (int)s.size());
    for (typename std::set<T,Tr,A>::const_iterator it = s.begin(); it != s.end(); ++it)
        doParsimPacking(buffer, *it);
}

template<typename T, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::set<T,Tr,A>& s)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        T x;
        doParsimUnpacking(buffer, x);
        s.insert(x);
    }
}

// Packing/unpacking an std::map
template<typename K, typename V, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::map<K,V,Tr,A>& m)
{
    doParsimPacking(buffer, (int)m.size());
    for (typename std::map<K,V,Tr,A>::const_iterator it = m.begin(); it != m.end(); ++it) {
        doParsimPacking(buffer, it->first);
        doParsimPacking(buffer, it->second);
    }
}

template<typename K, typename V, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::map<K,V,Tr,A>& m)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        K k; V v;
        doParsimUnpacking(buffer, k);
        doParsimUnpacking(buffer, v);
        m[k] = v;
    }
}

// Default pack/unpack function for arrays
template<typename T>
void doParsimArrayPacking(omnetpp::cCommBuffer *b, const T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimPacking(b, t[i]);
}

template<typename T>
void doParsimArrayUnpacking(omnetpp::cCommBuffer *b, T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimUnpacking(b, t[i]);
}

// Default rule to prevent compiler from choosing base class' doParsimPacking() function
template<typename T>
void doParsimPacking(omnetpp::cCommBuffer *, const T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimPacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

template<typename T>
void doParsimUnpacking(omnetpp::cCommBuffer *, T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimUnpacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

}  // namespace omnetpp

Register_Class(Hello)

Hello::Hello(const char *name, short kind) : ::Packet(name, kind)
{
}

Hello::Hello(const Hello& other) : ::Packet(other)
{
    copy(other);
}

Hello::~Hello()
{
    delete [] this->gateIndex;
    delete [] this->neighbours;
}

Hello& Hello::operator=(const Hello& other)
{
    if (this == &other) return *this;
    ::Packet::operator=(other);
    copy(other);
    return *this;
}

void Hello::copy(const Hello& other)
{
    this->gateIndexFrom = other.gateIndexFrom;
    delete [] this->gateIndex;
    this->gateIndex = (other.gateIndex_arraysize==0) ? nullptr : new int[other.gateIndex_arraysize];
    gateIndex_arraysize = other.gateIndex_arraysize;
    for (size_t i = 0; i < gateIndex_arraysize; i++) {
        this->gateIndex[i] = other.gateIndex[i];
    }
    delete [] this->neighbours;
    this->neighbours = (other.neighbours_arraysize==0) ? nullptr : new int[other.neighbours_arraysize];
    neighbours_arraysize = other.neighbours_arraysize;
    for (size_t i = 0; i < neighbours_arraysize; i++) {
        this->neighbours[i] = other.neighbours[i];
    }
    this->neighName = other.neighName;
    this->countRound = other.countRound;
    this->originalSource = other.originalSource;
}

void Hello::parsimPack(omnetpp::cCommBuffer *b) const
{
    ::Packet::parsimPack(b);
    doParsimPacking(b,this->gateIndexFrom);
    b->pack(gateIndex_arraysize);
    doParsimArrayPacking(b,this->gateIndex,gateIndex_arraysize);
    b->pack(neighbours_arraysize);
    doParsimArrayPacking(b,this->neighbours,neighbours_arraysize);
    doParsimPacking(b,this->neighName);
    doParsimPacking(b,this->countRound);
    doParsimPacking(b,this->originalSource);
}

void Hello::parsimUnpack(omnetpp::cCommBuffer *b)
{
    ::Packet::parsimUnpack(b);
    doParsimUnpacking(b,this->gateIndexFrom);
    delete [] this->gateIndex;
    b->unpack(gateIndex_arraysize);
    if (gateIndex_arraysize == 0) {
        this->gateIndex = nullptr;
    } else {
        this->gateIndex = new int[gateIndex_arraysize];
        doParsimArrayUnpacking(b,this->gateIndex,gateIndex_arraysize);
    }
    delete [] this->neighbours;
    b->unpack(neighbours_arraysize);
    if (neighbours_arraysize == 0) {
        this->neighbours = nullptr;
    } else {
        this->neighbours = new int[neighbours_arraysize];
        doParsimArrayUnpacking(b,this->neighbours,neighbours_arraysize);
    }
    doParsimUnpacking(b,this->neighName);
    doParsimUnpacking(b,this->countRound);
    doParsimUnpacking(b,this->originalSource);
}

int Hello::getGateIndexFrom() const
{
    return this->gateIndexFrom;
}

void Hello::setGateIndexFrom(int gateIndexFrom)
{
    this->gateIndexFrom = gateIndexFrom;
}

size_t Hello::getGateIndexArraySize() const
{
    return gateIndex_arraysize;
}

int Hello::getGateIndex(size_t k) const
{
    if (k >= gateIndex_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)gateIndex_arraysize, (unsigned long)k);
    return this->gateIndex[k];
}

void Hello::setGateIndexArraySize(size_t newSize)
{
    int *gateIndex2 = (newSize==0) ? nullptr : new int[newSize];
    size_t minSize = gateIndex_arraysize < newSize ? gateIndex_arraysize : newSize;
    for (size_t i = 0; i < minSize; i++)
        gateIndex2[i] = this->gateIndex[i];
    for (size_t i = minSize; i < newSize; i++)
        gateIndex2[i] = 0;
    delete [] this->gateIndex;
    this->gateIndex = gateIndex2;
    gateIndex_arraysize = newSize;
}

void Hello::setGateIndex(size_t k, int gateIndex)
{
    if (k >= gateIndex_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)gateIndex_arraysize, (unsigned long)k);
    this->gateIndex[k] = gateIndex;
}

void Hello::insertGateIndex(size_t k, int gateIndex)
{
    if (k > gateIndex_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)gateIndex_arraysize, (unsigned long)k);
    size_t newSize = gateIndex_arraysize + 1;
    int *gateIndex2 = new int[newSize];
    size_t i;
    for (i = 0; i < k; i++)
        gateIndex2[i] = this->gateIndex[i];
    gateIndex2[k] = gateIndex;
    for (i = k + 1; i < newSize; i++)
        gateIndex2[i] = this->gateIndex[i-1];
    delete [] this->gateIndex;
    this->gateIndex = gateIndex2;
    gateIndex_arraysize = newSize;
}

void Hello::appendGateIndex(int gateIndex)
{
    insertGateIndex(gateIndex_arraysize, gateIndex);
}

void Hello::eraseGateIndex(size_t k)
{
    if (k >= gateIndex_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)gateIndex_arraysize, (unsigned long)k);
    size_t newSize = gateIndex_arraysize - 1;
    int *gateIndex2 = (newSize == 0) ? nullptr : new int[newSize];
    size_t i;
    for (i = 0; i < k; i++)
        gateIndex2[i] = this->gateIndex[i];
    for (i = k; i < newSize; i++)
        gateIndex2[i] = this->gateIndex[i+1];
    delete [] this->gateIndex;
    this->gateIndex = gateIndex2;
    gateIndex_arraysize = newSize;
}

size_t Hello::getNeighboursArraySize() const
{
    return neighbours_arraysize;
}

int Hello::getNeighbours(size_t k) const
{
    if (k >= neighbours_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)neighbours_arraysize, (unsigned long)k);
    return this->neighbours[k];
}

void Hello::setNeighboursArraySize(size_t newSize)
{
    int *neighbours2 = (newSize==0) ? nullptr : new int[newSize];
    size_t minSize = neighbours_arraysize < newSize ? neighbours_arraysize : newSize;
    for (size_t i = 0; i < minSize; i++)
        neighbours2[i] = this->neighbours[i];
    for (size_t i = minSize; i < newSize; i++)
        neighbours2[i] = 0;
    delete [] this->neighbours;
    this->neighbours = neighbours2;
    neighbours_arraysize = newSize;
}

void Hello::setNeighbours(size_t k, int neighbours)
{
    if (k >= neighbours_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)neighbours_arraysize, (unsigned long)k);
    this->neighbours[k] = neighbours;
}

void Hello::insertNeighbours(size_t k, int neighbours)
{
    if (k > neighbours_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)neighbours_arraysize, (unsigned long)k);
    size_t newSize = neighbours_arraysize + 1;
    int *neighbours2 = new int[newSize];
    size_t i;
    for (i = 0; i < k; i++)
        neighbours2[i] = this->neighbours[i];
    neighbours2[k] = neighbours;
    for (i = k + 1; i < newSize; i++)
        neighbours2[i] = this->neighbours[i-1];
    delete [] this->neighbours;
    this->neighbours = neighbours2;
    neighbours_arraysize = newSize;
}

void Hello::appendNeighbours(int neighbours)
{
    insertNeighbours(neighbours_arraysize, neighbours);
}

void Hello::eraseNeighbours(size_t k)
{
    if (k >= neighbours_arraysize) throw omnetpp::cRuntimeError("Array of size %lu indexed by %lu", (unsigned long)neighbours_arraysize, (unsigned long)k);
    size_t newSize = neighbours_arraysize - 1;
    int *neighbours2 = (newSize == 0) ? nullptr : new int[newSize];
    size_t i;
    for (i = 0; i < k; i++)
        neighbours2[i] = this->neighbours[i];
    for (i = k; i < newSize; i++)
        neighbours2[i] = this->neighbours[i+1];
    delete [] this->neighbours;
    this->neighbours = neighbours2;
    neighbours_arraysize = newSize;
}

int Hello::getNeighName() const
{
    return this->neighName;
}

void Hello::setNeighName(int neighName)
{
    this->neighName = neighName;
}

int Hello::getCountRound() const
{
    return this->countRound;
}

void Hello::setCountRound(int countRound)
{
    this->countRound = countRound;
}

int Hello::getOriginalSource() const
{
    return this->originalSource;
}

void Hello::setOriginalSource(int originalSource)
{
    this->originalSource = originalSource;
}

class HelloDescriptor : public omnetpp::cClassDescriptor
{
  private:
    mutable const char **propertyNames;
    enum FieldConstants {
        FIELD_gateIndexFrom,
        FIELD_gateIndex,
        FIELD_neighbours,
        FIELD_neighName,
        FIELD_countRound,
        FIELD_originalSource,
    };
  public:
    HelloDescriptor();
    virtual ~HelloDescriptor();

    virtual bool doesSupport(omnetpp::cObject *obj) const override;
    virtual const char **getPropertyNames() const override;
    virtual const char *getProperty(const char *propertyName) const override;
    virtual int getFieldCount() const override;
    virtual const char *getFieldName(int field) const override;
    virtual int findField(const char *fieldName) const override;
    virtual unsigned int getFieldTypeFlags(int field) const override;
    virtual const char *getFieldTypeString(int field) const override;
    virtual const char **getFieldPropertyNames(int field) const override;
    virtual const char *getFieldProperty(int field, const char *propertyName) const override;
    virtual int getFieldArraySize(omnetpp::any_ptr object, int field) const override;
    virtual void setFieldArraySize(omnetpp::any_ptr object, int field, int size) const override;

    virtual const char *getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const override;
    virtual std::string getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const override;
    virtual omnetpp::cValue getFieldValue(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const override;

    virtual const char *getFieldStructName(int field) const override;
    virtual omnetpp::any_ptr getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const override;
};

Register_ClassDescriptor(HelloDescriptor)

HelloDescriptor::HelloDescriptor() : omnetpp::cClassDescriptor(omnetpp::opp_typename(typeid(Hello)), "Packet")
{
    propertyNames = nullptr;
}

HelloDescriptor::~HelloDescriptor()
{
    delete[] propertyNames;
}

bool HelloDescriptor::doesSupport(omnetpp::cObject *obj) const
{
    return dynamic_cast<Hello *>(obj)!=nullptr;
}

const char **HelloDescriptor::getPropertyNames() const
{
    if (!propertyNames) {
        static const char *names[] = {  nullptr };
        omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
        const char **baseNames = base ? base->getPropertyNames() : nullptr;
        propertyNames = mergeLists(baseNames, names);
    }
    return propertyNames;
}

const char *HelloDescriptor::getProperty(const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? base->getProperty(propertyName) : nullptr;
}

int HelloDescriptor::getFieldCount() const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? 6+base->getFieldCount() : 6;
}

unsigned int HelloDescriptor::getFieldTypeFlags(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeFlags(field);
        field -= base->getFieldCount();
    }
    static unsigned int fieldTypeFlags[] = {
        FD_ISEDITABLE,    // FIELD_gateIndexFrom
        FD_ISARRAY | FD_ISEDITABLE | FD_ISRESIZABLE,    // FIELD_gateIndex
        FD_ISARRAY | FD_ISEDITABLE | FD_ISRESIZABLE,    // FIELD_neighbours
        FD_ISEDITABLE,    // FIELD_neighName
        FD_ISEDITABLE,    // FIELD_countRound
        FD_ISEDITABLE,    // FIELD_originalSource
    };
    return (field >= 0 && field < 6) ? fieldTypeFlags[field] : 0;
}

const char *HelloDescriptor::getFieldName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldName(field);
        field -= base->getFieldCount();
    }
    static const char *fieldNames[] = {
        "gateIndexFrom",
        "gateIndex",
        "neighbours",
        "neighName",
        "countRound",
        "originalSource",
    };
    return (field >= 0 && field < 6) ? fieldNames[field] : nullptr;
}

int HelloDescriptor::findField(const char *fieldName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    int baseIndex = base ? base->getFieldCount() : 0;
    if (strcmp(fieldName, "gateIndexFrom") == 0) return baseIndex + 0;
    if (strcmp(fieldName, "gateIndex") == 0) return baseIndex + 1;
    if (strcmp(fieldName, "neighbours") == 0) return baseIndex + 2;
    if (strcmp(fieldName, "neighName") == 0) return baseIndex + 3;
    if (strcmp(fieldName, "countRound") == 0) return baseIndex + 4;
    if (strcmp(fieldName, "originalSource") == 0) return baseIndex + 5;
    return base ? base->findField(fieldName) : -1;
}

const char *HelloDescriptor::getFieldTypeString(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeString(field);
        field -= base->getFieldCount();
    }
    static const char *fieldTypeStrings[] = {
        "int",    // FIELD_gateIndexFrom
        "int",    // FIELD_gateIndex
        "int",    // FIELD_neighbours
        "int",    // FIELD_neighName
        "int",    // FIELD_countRound
        "int",    // FIELD_originalSource
    };
    return (field >= 0 && field < 6) ? fieldTypeStrings[field] : nullptr;
}

const char **HelloDescriptor::getFieldPropertyNames(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldPropertyNames(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

const char *HelloDescriptor::getFieldProperty(int field, const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldProperty(field, propertyName);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

int HelloDescriptor::getFieldArraySize(omnetpp::any_ptr object, int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldArraySize(object, field);
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndex: return pp->getGateIndexArraySize();
        case FIELD_neighbours: return pp->getNeighboursArraySize();
        default: return 0;
    }
}

void HelloDescriptor::setFieldArraySize(omnetpp::any_ptr object, int field, int size) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldArraySize(object, field, size);
            return;
        }
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndex: pp->setGateIndexArraySize(size); break;
        case FIELD_neighbours: pp->setNeighboursArraySize(size); break;
        default: throw omnetpp::cRuntimeError("Cannot set array size of field %d of class 'Hello'", field);
    }
}

const char *HelloDescriptor::getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldDynamicTypeString(object,field,i);
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        default: return nullptr;
    }
}

std::string HelloDescriptor::getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValueAsString(object,field,i);
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndexFrom: return long2string(pp->getGateIndexFrom());
        case FIELD_gateIndex: return long2string(pp->getGateIndex(i));
        case FIELD_neighbours: return long2string(pp->getNeighbours(i));
        case FIELD_neighName: return long2string(pp->getNeighName());
        case FIELD_countRound: return long2string(pp->getCountRound());
        case FIELD_originalSource: return long2string(pp->getOriginalSource());
        default: return "";
    }
}

void HelloDescriptor::setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValueAsString(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndexFrom: pp->setGateIndexFrom(string2long(value)); break;
        case FIELD_gateIndex: pp->setGateIndex(i,string2long(value)); break;
        case FIELD_neighbours: pp->setNeighbours(i,string2long(value)); break;
        case FIELD_neighName: pp->setNeighName(string2long(value)); break;
        case FIELD_countRound: pp->setCountRound(string2long(value)); break;
        case FIELD_originalSource: pp->setOriginalSource(string2long(value)); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Hello'", field);
    }
}

omnetpp::cValue HelloDescriptor::getFieldValue(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValue(object,field,i);
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndexFrom: return pp->getGateIndexFrom();
        case FIELD_gateIndex: return pp->getGateIndex(i);
        case FIELD_neighbours: return pp->getNeighbours(i);
        case FIELD_neighName: return pp->getNeighName();
        case FIELD_countRound: return pp->getCountRound();
        case FIELD_originalSource: return pp->getOriginalSource();
        default: throw omnetpp::cRuntimeError("Cannot return field %d of class 'Hello' as cValue -- field index out of range?", field);
    }
}

void HelloDescriptor::setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValue(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        case FIELD_gateIndexFrom: pp->setGateIndexFrom(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_gateIndex: pp->setGateIndex(i,omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_neighbours: pp->setNeighbours(i,omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_neighName: pp->setNeighName(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_countRound: pp->setCountRound(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_originalSource: pp->setOriginalSource(omnetpp::checked_int_cast<int>(value.intValue())); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Hello'", field);
    }
}

const char *HelloDescriptor::getFieldStructName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructName(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    };
}

omnetpp::any_ptr HelloDescriptor::getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructValuePointer(object, field, i);
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        default: return omnetpp::any_ptr(nullptr);
    }
}

void HelloDescriptor::setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldStructValuePointer(object, field, i, ptr);
            return;
        }
        field -= base->getFieldCount();
    }
    Hello *pp = omnetpp::fromAnyPtr<Hello>(object); (void)pp;
    switch (field) {
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Hello'", field);
    }
}

namespace omnetpp {

}  // namespace omnetpp

