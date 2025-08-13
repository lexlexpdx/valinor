# General strategies for CTF

1. Use "file" command for every new file to view file data
2. Search for strings using string | grep pipe
3. Binwalk will search binary images for embedded files and exe codes
4. Use exiftool to find metadata information for file
5. Cyberchef allows for all kinds of conversions
6. Use zsteg for analyzing images to find hidden data (steganography)
7. Remember that you can often redirect output to a file of your choice and then look at it that way!!
8. You can use "find" to find a file in a hierarchy
	- ``find . -name file.txt``
9. Grep
	- you can pipe strings into grep and use ``-v`` to "invert the sense of matching" which will omit any lines containing characters you specify
	- ex: ``strings text.pcap | grep -v 'XOn\|1234'`` will omit any lines that have "XOn" or "1234"
		- In this example ``\|`` is an OR operator
	- This is particularly useful on pcap files

## Disk Analysis
1. Main layers of disk images:
	1. **Media**
		- All media layer tools start with "mm"
		- use mmls to get the partition table of the image and other info
		- Lowest level, provides access info for deeper layers
	2. **Block**
		- second lowest level
		- All Block layer tools start with "blk"
		- blkcat will give contents of a single block
		- All broken into equal-sized chunks
	3. **Inode**
		- This is the bookkeeping layer of the image
		- Tools for this layer start with "i"
		- Kinda works like a table of contents
		- icat is like cat for the filename layer, but outputs the contents of a file based on the inode number
			- when using icat, you can extract a file like this:
				- ``icat -o 123456 file.img 123 > output.txt``
				- then if that is encrypted, run openssl on it
	4. **Filename**
		- This is the layer the user usually sees
		- Most interactions with the filename layer use regular shell commands
		- All tools for this layer start with "f"
		
2. Sleuthkit
	- To solve problems with an instance, use the given access checker program
	- If asked for length in sectors: use the information from the file command
	- Netcat (NC)
		- Can be used for TCP, UDP
		- TCP (Transmission Control Protocol)
			- Enables programs and devices to exchange messages over a network
			- Can send packets across the internet
			- Very common usage and ensures end-to-end data delivery
				- Delivered in send order and not corrupted
			- Is a connection-oriented protocol
			- Used by SSH, FTP, SB/CIFS
			- Is protocol number 0x6 in the IP suite
		- UDP (User Datagram Protocol)
			- Connectionless protocol
			- Often used for streaming media
				- This is because mis-ordering and minor packet loss is acceptable with these services
			- Used for DNS, DHCP
			- Is protocol number 0x11 in the IP suite
		- Typically in the following format:
			- nc <destination> port
			- Ex: nc saturn.picoctf.net 52279
	- fls
		- use "-o" for sector offset
		- Look for linux, or other os systems as clues
		- You can also look for largest partitions with uneven lengths as clues forwhere to start
		- fls will dump all top-level directories of the disk image
		- Look at folders that have user influece, like root and home
		- If a file or folder as (realloc) that means it has been deleted or moved

## Metadata

1. When looking for metadata, look at all pieces (use exiftool) to see if there is anything funky


## Base64-encoded strings

1. Always a multiple of 4
	- use echo piped through wc to count the number of chars in a string
	- ex: ``echo -n "cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9" | wc -m``
		- "-n" prevents newline
		- wc counts lines, words, chars, etc (-m is chars)
2. Only uses "A" to "Z", "a" to "z", "0" to "9", and "+" "/"
3. End of a string can be padded up to two times using the "=" char (allowed at end only)
4. Use cyberchef to decode potential Base64-encoded strings
	- Two other options for decoding Base64-encoded strings:
		- ``base64 -d <<< string``
			- "-d" is the flag for decode
		- ``openssl base64 -d <<< string``
5. Using base64 command


## Openssl
1. Openssl encrypts files using various encryption schemes
2. Usually formatted like this:
	- ``openssl <encryption scheme> -d -in <file_to_decrypt> -out <output_file>``
	- "-d" allows a decrypt
	- you can also use -k to put in the password, or it will prompt 

## Packet Analysis
1. Also known as network analysis
	- Understand what has happened on a network through analyzing captured packets
	- We will use wireshark
2. How to use packet analysis
	- Packet analysis is all about filtering
	- You can almost always filter out ARP (Address resolution protocol) messages because these are messages that just relate to IP addresses and hardware addresses
	- Filtering with wireshark
		- To filter out, go to the filter line and use "!" and the filter you want to apply
		- Example: If I want to filter out ARP messages, I would use !arp
	- TCP Handshake (Three way handshake)
		- This can be identified by flags in packets
		1. SYN from host A
			- SYN = synchronization
		2. SYN, ACK from host B
			- ACK = acknowledgement
		3. Ack from host A
	- Look at packets that do not have TCP handshake flags
	- To inspect a packet, double click on the packet
	- If you see things like a protocol that stands out and is the only one, inspect those further
	- Filter as many packets as you can, and then look for oddities

## Wireshark
1. Apply filters!
	- See above for some common ones
	- If you notice that packets have base64 data, add a filter that has the protocol and contains "=="
		- ex: ``tcp contains "=="``

## Using awk
1. awk is a language that takes whitespace separated input files (columns), matches them against patters, and executes code for each match
2. Base syntax
	- ``awk 'BEGIN { start_block } pattern { action } END { end_block }' file`` 
3. Print
	- You can print a column, or multiple columns using the ``print`` command
		- Example: ``awk '{ print $0 }' file.txt`` will print the first column of the file.txt file
	- If you want to print a space in between two columns, you can do that by adding " " 
		- Example: ``awk '{ print $1 " " $2 }' file.txt`` will print the first column and second column of the file separated by a single space
	- You can also use pattern matching with awk.
		- Let's say I want to print a phone number for every person named "Bill" in the first column of my text. Assume that phone numbers are listed in column 2
		- Example: ``awk '$1 == "Bill" { print $2 }' text.txt``
		- To do multiple patterns the syntax is: ``awk pattern1 { code1 } pattern2 {code2}``
			- Example: ``awk '$1 == "Bill" { print $1 } $2 == "555-3430" { print $1 }' mail.txt`` This will print all phone numbers that match "Bill" as the name, and all names that match the phone number "555-3430"
	- awk variables can be initialized in a ``BEGIN``, and ``END`` 
	- Incrementing with variables
		- Let's say I want to sum the length of all names in a list (column 1), I could do this using awk variables as well as a length() function within awk
			- Example: ``awk '{ s += length($1) }' END { print s }' text.txt`` This will add the length of each name in the list to the variable ``s`` and then print ``s`` at the end of the list
	- Using regex to find patterns
		- Let's say I want to find any words containing vowels. I can use a regex expression to indicate this:
			- Example: ``awk '$1 ~ /^[AEIOUY]aeioy]+$/ { print $1 }' text.txt`` This sees if anything in column 1 matches the regex expression provided and then prints any matches.
			- ``~`` is the regex match operator
			- For instance: ``$1 ~ /foo/`` "does the info in column 1 match /foo/
			- You can also use ``!~`` to exclude matches
	- Control flow is also an option with awk
		- general syntax is: ``awk '{ if (condition) { do this } else { do that }} file.txt``
		- If there is no else, you do not need to use an if
	- Logical operators of ``&&`` and ``||`` work in awk as well
	- Mod and integer division is also supported
	- Builtins (variables that are predetermined)
		- FS: Field separator
		- RS: Record separator
		- NF: Number of columns (fields)
		- NR: Index of current row (record)
		- $0: Full line (all columns)
	- Flags
		- ``-F``
			- example: ``awk -F:`` separates columns by colon
		- ``-f``
			- example: ``awk -f script.awk``
				- Loads awk script from the file instead of command line
		- ``-v``
			- example: ``awk -v init=1``
				- Variable init begins at 1 instead of default 0 
	
	
## Network Layers
1. **Application Layer**
	- This layer handles data traffic between applications
	- HTTP is in this layer: used to obtain web pages
	- In Wireshark you can see the layer on the middle panel breakdown
2. **Transport Layer**
	- This layer is responsible for providing connections on the same host, allowing for several applications on the same device to have a different connection
	- Defines functionality for reliable transport
	- Two protocols are used on this layer:
		1. **TCP**
			- Used when you need to ahve reliable transport
		2. **UDP**
			- Used when you don't need reliable transport
			- Often used for voice communication
	- Each connection is assigned to a port, which allos it to tell the difference between connections in the same computer.
3. **Network Layer**
	- Provides devices with an address in the network (IP address)
	- Routes info through different routers
	- Maps connections between all the computers connected to the internet
4. **Data Link Layer**
	- Provides communication between devices that are connected directly
	- Ethernet and Wifi are protocols in the data link layer
		- MAC addresses specify a physical address on ethernet or wifi
		- MAC addresses can change depending on the network you are connected to
5. **Physical Layer**
	- Handles electrical pulses on the wire that represent bits	

## Python Programming
1. **Hexadecimal representation**
	- To print a hex representation of a number in a string you can use ``\x`` which tells python that the following two characters are a hex number
2.
=======
## Zbarimg
1. Uses zbar-tools to scan and decode various barcode formats
2. To install:
	- ```sudo apt-get install zbar-tools```
3. When you want to try to decode an image use:
	- ```zbarimg your_file.png```
