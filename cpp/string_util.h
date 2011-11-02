#ifndef _HPS_NANOMUNCHERS_STRING_UTIL_H_
#define _HPS_NANOMUNCHERS_STRING_UTIL_H_
#include <algorithm>
#include <functional>
#include <cctype>
#include <string>

namespace hps
{
namespace util
{

/// <summary> Extract typed, formatted input from a string. </summary>
template <typename Type>
inline void ExtractToken(const std::string& token, Type* out)
{
  assert(out);
  std::stringstream ssToken(token);
  ssToken >> *out;
}

// reissb -- 20111102 -- String trim functions taken from:
//   http://stackoverflow.com/questions/216823/whats-the-best-way-to-trim-stdstring
/// <summary> Trim from start. </summary>
inline std::string& LTrim(std::string* s)
{
  assert(s);
  s->erase(s->begin(), std::find_if(s->begin(), s->end(),
           std::not1(std::ptr_fun<int, int>(std::isspace))));
  return *s;
}
/// <summary> Trim from end. </summary>
inline std::string& RTrim(std::string* s)
{
  assert(s);
  s->erase(std::find_if(s->rbegin(), s->rend(),
           std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s->end());
  return *s;
}
/// <summary> Trim from both ends. </summary>
inline std::string& Trim(std::string* s)
{
  assert(s);
  return LTrim(&RTrim(s));
}

}
using namespace util;
}

#endif //_HPS_NANOMUNCHERS_STRING_UTIL_H_
