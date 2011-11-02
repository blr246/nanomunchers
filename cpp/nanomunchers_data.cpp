#include "nanomunchers_data.h"
#include "nanomunchers_serialize.h"
#include <iostream>
#include <algorithm>
#include <functional>

namespace hps
{
namespace nano
{

void WriteMuncherList(const MuncherList& munchers, std::ostream* stream)
{
  assert(stream);
  *stream << munchers.size() << std::endl;
  for (MuncherList::const_iterator muncher = munchers.begin();
       muncher != munchers.end();
       ++muncher)
  {
    Serialize(*muncher, stream);
  }
}

}
}
