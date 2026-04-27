CC = gcc
CFLAGS = -Wall -I../c-socketUtils

TARGET = client.exe
SRCS = main.c ../c-socketUtils/socketutil.c

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

clean:
	rm -f $(TARGET)
