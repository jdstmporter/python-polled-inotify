CXX := g++
CXXFLAGS := -std=c++14 -O0 -g3 -Wall -c -fmessage-length=0
DEBUGFLAGS := -pg
OBJ := $(addprefix src/notifier/,errors.o mask.o notifier.o event.o main.o)


	
inote: $(OBJ)
	$(CXX) $(LKRFLAGS) $(DEBUGFLAGS) -o inote $(OBJ)
	
	
%.o: %.c
	cd src/notifier; $(CXX) $(CXXFLAGS) $(DEBUGFLAGS) -c $@ $<
	
clean: 
	cd src/notifier;rm -f *.o
	