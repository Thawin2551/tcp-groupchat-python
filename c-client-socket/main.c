#include "../c-socketUtils/socketutil.h"

int main() {

    int socketFD = createTCPIpv4Socket();
    struct sockaddr_in* address = createIpv4Address("127.0.0.1", 2000);

    int result = connect(socketFD, (const struct sockaddr*)address, sizeof(*address));

    if (result == 0) {
        printf("Connection was Successful !\n");
    } else {
        perror("Connection Failed !\n");
        return 1; // exit the program to prevent crash in future
    };


    char* name = NULL;
    size_t nameSize = 0;
    printf("Please enter your name: ");
    ssize_t nameCount = getline(&name, &nameSize, stdin);
    name[nameCount - 1] = 0; // remove new line character

    char* line = NULL;
    size_t lineSize = 0;
    printf("type and we will send (type exit)...\n");

    // this function will receive message from server and print it on the console
    startListeningAndPrintMessagesOnNewThread(socketFD);
    
    char buffer[1024];


    // Loop send message in the client side
    while (1) {

        ssize_t charCount = getline(&line, &lineSize, stdin);
        if (charCount <= 0) continue;
        line[charCount - 1] = 0; // remove new line character

        if (strcmp(line, "exit") == 0) { // strcmp returns 0 when strings are exactly equal
            sprintf(buffer, "%s: exit\n", name);
            send(socketFD, buffer, strlen(buffer), 0); // SEND 'exit' TO SERVER
            break; 
        } 

        sprintf(buffer, "%s: %s\n", name, line); // format "name: message"
        send(socketFD, buffer, strlen(buffer), 0); // send buffer (with name), not raw line
    }   
    
    close(socketFD);
    free(address); // free the memory allocated for address

    return 0;
}