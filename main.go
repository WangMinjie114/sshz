package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"golang.org/x/crypto/ssh"
	"net"
	"os"
	"strings"
	"time"
)

var(
	filename string = "host_mess.txt"
	filelist string = "host_list.txt"
)

type host_mess_type struct {
	Ip			string	`json:"IP"`
	Cname       string 	`json:"cname"`
	Username    string	`json:"username"`
	Password 	string	`json:"passwd"`
	Port 		int		`json:"port"`
	Is_key 		bool	`json:"is_key"`
	Can_connect bool	`json:"can_connect"`
}

func err_check(e error) {
	if e != nil {
		fmt.Println(e)
	}
}

func input_mess(outmess string) string {
	inputReader := bufio.NewReader(os.Stdin)
	fmt.Printf("%s", outmess)
	input, err := inputReader.ReadString('\n')
	err_check(err)
	return strings.Trim(input, "\n")
}

func ssh_connect( user, password, host string, port int ) ( *ssh.Session, error ) {
	var (
		auth         []ssh.AuthMethod
		addr         string
		clientConfig *ssh.ClientConfig
		client       *ssh.Client
		session      *ssh.Session
		err          error
	)
	// get auth method
	auth = make([]ssh.AuthMethod, 0)
	auth = append(auth, ssh.Password(password))
	hostKeyCallbk := func(hostname string, remote net.Addr, key ssh.PublicKey) error {
		return nil
	}
	clientConfig = &ssh.ClientConfig{
		User:               user,
		Auth:               auth,
		Timeout:             30 * time.Second,
		HostKeyCallback:    hostKeyCallbk,
	}
	// connet to ssh
	addr = fmt.Sprintf( "%s:%d", host, port )
	if client, err = ssh.Dial( "tcp", addr, clientConfig ); err != nil {
		return nil, err
	}
	// create session
	if session, err = client.NewSession(); err != nil {
		return nil, err
	}
	return session, nil
}

func create_file(filename string) (int, error) {
	new_file, err := os.Create(filename)
	if err != nil {
		fmt.Println(err)
		return 1, err
	}
	new_file.Close()
	return 0, nil
}

func check_file_is_exist(filename string) int {
	file_info, _ := os.Stat(filename)
	if file_info == nil {
		fmt.Println("file %s don't exist, will create it.", filename)
		create_status, err := create_file(filename)
		if create_status == 0 {
			return 0
		} else {
			fmt.Println("File created error, %s", err)
			return 1
		}
	}
	return 0
}

func write_file(filename, message string) int {
	file_status := check_file_is_exist(filename)
	if file_status == 0 {
		file, err := os.OpenFile(filename, os.O_WRONLY|os.O_APPEND, 0666, )
		err_check(err)
		defer file.Close()
		// 写字节到文件中
		byteSlice := []byte(message + "\n")
		_, err = file.Write(byteSlice)
		err_check(err)
	}
	return 0
}

func mess(status string) int {
	if status == "add" {
		ip := input_mess("Please input ip >")
		username := input_mess("Please input username >")
		//is_key := input_mess("Whether to log in with the secret key？[y/n]")
		//fmt.Println(is_key)
		passwd := input_mess("Please input password >")
		session, err := ssh_connect(username, passwd, ip, 22)
		if err != nil {
			fmt.Println(err)
			return 1
		} else {
			defer session.Close()
			fmt.Println("connect success")
			cname := input_mess("Please input cname default:'' >")
			// 存入文件
			var host_msg *host_mess_type = new(host_mess_type)
			host_msg.Cname = cname
			host_msg.Ip = ip
			host_msg.Is_key= false
			host_msg.Username = username
			host_msg.Password = passwd
			host_msg.Port = 22
			host_msg.Can_connect = true
			fmt.Println(host_msg)
			b, err := json.Marshal(host_msg)
			err_check(err)
			write_file(filename, string(b))
		}
	} else if status == "update" {

	} else {
		fmt.Println("status error")
		return 3
	}
	return 0
}

func main() {
	status := "add"
	mess(status)
	//write_file("test123.txt", "12345671234567")
}
