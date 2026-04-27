#include "socketutil.h"

struct AcceptedSocket acceptedSockets[10];
int acceptedSocketCount = 0;

// create a TCP socket
int createTCPIpv4Socket() { return socket(AF_INET, SOCK_STREAM, 0); }
// create a IPv4 addressz
struct sockaddr_in* createIpv4Address(char* ip, int port) {
    struct sockaddr_in* address = (struct sockaddr_in*)malloc(sizeof(struct sockaddr_in));
    address->sin_family = AF_INET;
    address->sin_port = htons(port);
    
    // condition ip
    if (strlen(ip) == 0) {
        address -> sin_addr.s_addr = INADDR_ANY; // address any we will listen to any coming ip
    } else {
        inet_pton(AF_INET, ip, &address->sin_addr.s_addr);
    }

    return address;
}


// accept the incoming connection
struct AcceptedSocket* acceptIncomingConnection(int serverSocketFD) {
    struct sockaddr_in clientAddress; // just sent a clientAddress not sockaddr_in* clientAddress
    int clientAddress_size = sizeof(struct sockaddr_in);
    int clientSocketFD = accept(serverSocketFD, (struct sockaddr*)&clientAddress, (socklen_t*)&clientAddress_size);
    
    struct AcceptedSocket* acceptedSocket = malloc(sizeof(struct AcceptedSocket));
    
    acceptedSocket -> address = clientAddress;
    acceptedSocket -> acceptedSocketFD = clientSocketFD;
    acceptedSocket -> acceptedSuccessfully = clientSocketFD > 0;

    if (!acceptedSocket -> acceptedSuccessfully) {
        perror("Accept incoming connection failed\n");
        acceptedSocket -> error = clientSocketFD;
    }

    return acceptedSocket;

}

// print message from the client server and send a message back to client
void* receiveMessageAndPrint(void* arg) {
    // Cast the generic void pointer back to our struct
    struct AcceptedSocket* clientSocket = (struct AcceptedSocket*)arg;
    char buffer[1024]; // create buffer string for receiving message from client

    while (1) 
    {
        ssize_t amountRecieved = recv(clientSocket -> acceptedSocketFD, buffer, 1023, 0);
    
        if (amountRecieved > 0) {
            buffer[amountRecieved] = '\0'; // add null-terminated at the end of the string
            printf("(Client) %s", buffer); // change the "response" to "Client" to see the message that sent from client side
             
            sendReceiveMessageToTheOtherClient(buffer, clientSocket -> acceptedSocketFD);

            // if the client (user) send "exit" to the server, this condition will compare string and return if input equal to "exit" (0)
            if (strcmp(buffer, "exit\n") == 0) {
                printf("Exit command received. Shutting down server!\n");
                exit(0); // Kills the entire C program
            }

            char* reply = "Message received!\n";
            send(clientSocket -> acceptedSocketFD, reply, strlen(reply), 0);
        } else { // if amountRecieved == 0 or -1 it mean that the client is disconnected or the server is unable to receive message
            printf("--- Client disconnected or receiving message failed. ---\n");
            break;
        }
    }

    close(clientSocket -> acceptedSocketFD);
    free(clientSocket); // Free memory when done
    return NULL;
}

void sendReceiveMessageToTheOtherClient(char* buffer, int socketFD) {
    for (int i = 0; i < acceptedSocketCount; i++) {
        if (acceptedSockets[i].acceptedSocketFD != socketFD) { // we will sent the message to other clients except the client who sent the message
            send(acceptedSockets[i].acceptedSocketFD, buffer, strlen(buffer), 0);
        }
    }
}

// start accepting incoming connections
void startAcceptingIncomingConnections(int serverSocketFD) {

    while (1) {
        struct AcceptedSocket* clientSocket = acceptIncomingConnection(serverSocketFD);
        acceptedSockets[acceptedSocketCount++] = *clientSocket;
         
        receiveMessageAndPrintOnSeperateThread(clientSocket);
    }
}

// receive message and print on seperate thread
void receiveMessageAndPrintOnSeperateThread(struct AcceptedSocket* pSocket) {

    pthread_t id;
    pthread_create(
        &id,
        NULL,
        receiveMessageAndPrint,
        pSocket // Pass the struct pointer directly
    );
    pthread_detach(id);
}

void* ListenAndPrint(void* socketFDVoid) {
    int socketFD = *(int*)socketFDVoid;
    free(socketFDVoid); // free the heap-allocated int
    char buffer[1024];

    while (1) 
    {
        ssize_t amountRecieved = recv(socketFD, buffer, 1023, 0);
    
        if (amountRecieved > 0) {
            buffer[amountRecieved] = '\0';
            printf("%s", buffer);
            fflush(stdout); // flush immediately to see the message right away in other client terminal except sender
        } else {
            printf("--- Disconnected from server. ---\n");
            break;
        }
    }

    close(socketFD);
    return NULL;
}

void startListeningAndPrintMessagesOnNewThread(int socketFD) {

    // Allocate on the heap so the pointer is still valid after this function returns
    int* pSocketFD = malloc(sizeof(int));
    *pSocketFD = socketFD;

    pthread_t id;
    pthread_create(
        &id,
        NULL,
        ListenAndPrint,
        pSocketFD
    );

    pthread_detach(id);
}

    
