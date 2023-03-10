// Generated by yaCCM
// File test.hpp

#ifndef _TEST_HPP_
#define _TEST_HPP_

#include "yaCCM_runtime.hpp"

//START_303b7efb21785f19b1820de8ec4a2c90148c89b5d1f4999c16498126
//STOP

#include "toto.hpp"

typedef float speed;

virtual void activate ()=0;
namespace TEST_MODULE {
	typedef long MyInt;
	
	typedef enum Couleur {
		BLEU,
		BLANC,
		ROUGE
	};
	
	//Definition of MyStruct
	struct MyStruct {
		long 	id;
		float 	val;
	};
	
	typedef std::vector<MyStruct,13> seq_MyStruct;
	
	typedef union  {
		MyInt 	bleu;
		seq_MyStruct 	white;
		float 	red;
	} Msg ;
	
	class iService {
		public:
			iService() {};
			virtual ~iService() {};
		virtual int functionWith1Arg (MyInt val)=0;
		virtual int functionWith2Args (MyInt arg1 , float& arg2)=0;
	};
	
	//START_d7215dd05a56c1009ae91cf9367bf5e31cf45156fbb47bdb4755b06f
	//STOP
};



#endif // _TEST_HPP_