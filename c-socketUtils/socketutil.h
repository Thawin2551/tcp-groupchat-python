#ifndef SOCKETUTIL_H
#define SOCKETUTIL_H

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <malloc.h>
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h>

// define a struct type of AcceptedSocket that contain in struct, sockadddr_in, error, boolean
typedef struct AcceptedSocket {
    int acceptedSocketFD;
    struct sockaddr_in address; // the ip address of the client
    int error; // if the connection is failed it will return the error
    bool acceptedSuccessfully; // if the connection is successful it will return true (bytes > 0)
} AcceptedSocket;

// define a array to accept the incoming connection
extern struct AcceptedSocket acceptedSockets[10];
extern int acceptedSocketCount;

// define a function before using in main
int createTCPIpv4Socket();
struct sockaddr_in* createIpv4Address(char* ip, int port);
struct AcceptedSocket* acceptIncomingConnection(int serverSocketFD);
void* receiveMessageAndPrint(void* arg); // socket file descriptor
void startAcceptingIncomingConnections(int serverSocketFD);
void receiveMessageAndPrintOnSeperateThread(struct AcceptedSocket* clientSocket);
void sendReceiveMessageToTheOtherClient(char* buffer, int socketFD);
void startListeningAndPrintMessagesOnNewThread(int socketFD);
void* ListenAndPrint(void* socketFDVoid);

#endif
