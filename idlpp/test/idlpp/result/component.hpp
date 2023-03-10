// Generated by yaCCM
// File component.hpp

#ifndef _COMPONENT_HPP_
#define _COMPONENT_HPP_

#include "yaCCM_runtime.hpp"

//START_671633ba9fd09dc7153f26c0dd0febeeab9907d86c6ad0f79be96008
//STOP

#include "Interface.hpp"

namespace Boids_Module {
	class Component : public virtual yaCCM::Component{
	public:
		// TODO Manage attribute
	
		//Destructor
		virtual ~Component(){};
		
		//Facet accesors
		virtual iService& get_facet()=0;
		
		//Receptables connectors
		void connect_receptacle(Module::iProvide& receptacle) {this->receptacle = &receptacle;};
		
	private:
		Module::iProvide* receptacle;
	
		//START_7ebbb7092621fbfb549049f79d91e0b6d9e5d7e8693bbfa69ab9d307_private
		//STOP
	};
	//START_53fe11feadf2519c01a223ab17ee8042e4d06bf129467e7351578ffb
	//STOP
};



#endif // _COMPONENT_HPP_