package main

import (
    "log"
    "crypto/tls"
    "net"
    "bufio"
)

const length = 10000000
var data []byte

func main() {
    log.SetFlags(log.Lshortfile)

    cer, err := tls.LoadX509KeyPair("server.crt", "server.key")
    if err != nil {
        log.Println(err)
        return
    }

    config := &tls.Config{Certificates: []tls.Certificate{cer}}
    ln, err := tls.Listen("tcp", ":4431", config) 
    if err != nil {
        log.Println(err)
        return
    }
    defer ln.Close()

	data = make([]byte, length)
	for i :=0; i < length ;i++ {
		data[i] = 1
	}
    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Println(err)
            continue
        }
        go handleConnection(conn)
    }
}

func handleConnection(conn net.Conn) {
    defer conn.Close()
    r := bufio.NewReader(conn)
    for {
        msg, err := r.ReadString('\n')
        if err != nil {
            log.Println(err)
            return
        }

        println(msg)

        n, err := conn.Write(data)
        if err != nil {
            log.Println(n, err)
            return
        }
    }
}