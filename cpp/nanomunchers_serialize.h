#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#include "nanomunchers_data.h"
#include <vector>
#include <iosfwd>
#include <assert.h>

namespace hps
{
namespace nano
{

/// <summary> Serialize a muncher to string. </summary>
bool Serialize(const Muncher& muncher, std::ostream* stream);

/// <summary> Deserialize a muncher from string. </summary>
bool Deserialize(std::istream* stream, Muncher* muncher);

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
