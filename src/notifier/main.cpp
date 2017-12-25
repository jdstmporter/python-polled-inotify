/*
 * main.cpp
 *
 *  Created on: 29 Jun 2014
 *      Author: julianporter
 */

#include <iostream>
#include <list>

#include "notifier.hpp"

int main(int argc, char *argv[]) {

	notify::Notifier n;
	n.addPath("/home/julianporter/");
	unsigned ticks=0;

	while(ticks<20) {
		auto got=n.waitForEvent(1000);
		if(got) {
			auto nEvents=n.nEvents();
			auto events=n.getEvents();
			std::cout << "Got " << nEvents << " events (" << events.size() << ")" << std::endl;

			for(auto it=events.begin();it!=events.end();it++) {
				std::cout << "Mask " << it->mask << " " << *it << "    "<< it->path << std::endl;
			}
		}
		else {
			std::cout << ".";
		}
		ticks++;
		std::cout.flush();
	}
	return 0;
}



