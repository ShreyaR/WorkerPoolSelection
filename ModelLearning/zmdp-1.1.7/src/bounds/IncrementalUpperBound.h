/********** tell emacs we use -*- c++ -*- style comments *******************
 $Revision: 1.1 $  $Author: trey $  $Date: 2006/10/24 02:06:35 $
   
 @file    IncrementalUpperBound.h
 @brief   No brief

 Copyright (c) 2006, Trey Smith.

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License.  You may
 obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 implied.  See the License for the specific language governing
 permissions and limitations under the License.

 ***************************************************************************/

#ifndef INCIncrementalUpperBound_h
#define INCIncrementalUpperBound_h

#include <iostream>
#include <string>
#include <vector>

#include "AbstractBound.h"
#include "MDPCache.h"

using namespace sla;

namespace zmdp {

struct IncrementalUpperBound : public AbstractBound {
  virtual void initNodeBound(MDPNode& cn) = 0;
  virtual void update(MDPNode& cn, int* maxUBActionP) = 0;
};

}; // namespace zmdp

#endif // INCIncrementalUpperBound_h

/***************************************************************************
 * REVISION HISTORY:
 * $Log: IncrementalUpperBound.h,v $
 * Revision 1.1  2006/10/24 02:06:35  trey
 * initial check-in
 *
 *
 ***************************************************************************/

