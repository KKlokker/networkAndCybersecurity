import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Scanner;

public class sockets {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String command = input.nextLine();
        if(command.equals("TCPServer"))
            startTCPServer();
        if(command.equals("TCPClient"))
            connectToTCPServer();
        if(command.equals("UDPServer"))
            startUDPServer();
        if(command.equals("UDPClient"))
            connectToUDPServer();
        input.close();
    }

    private static void connectToTCPServer() {
        Socket socket = null;
        InputStreamReader ISR = null;
        OutputStreamWriter OSW = null;
        BufferedReader BR = null;
        BufferedWriter BW = null;
        Scanner scanner = null;
        
        try {
            socket = new Socket("localhost",1234);
            ISR = new InputStreamReader(socket.getInputStream());
            OSW = new OutputStreamWriter(socket.getOutputStream());
            BR = new BufferedReader(ISR);
            BW = new BufferedWriter(OSW);

            scanner = new Scanner(System.in); 
            while(true) {
                String command = scanner.nextLine();
                BW.write(command);
                BW.newLine();
                BW.flush();

                System.out.println("Response: " + BR.readLine());
            }
        }
        catch(IOException e) {
            e.printStackTrace();
        }
        finally {
            try {
                if(socket != null) socket.close();
                if(ISR != null) ISR.close();
                if(OSW != null) OSW.close();
                if(BR != null) BR.close();
                if(BW != null) BW.close();
                if(scanner != null) scanner.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private static void startTCPServer() {
        Socket socket = null;
        InputStreamReader ISR = null;
        OutputStreamWriter OSW = null;
        BufferedReader BR = null;
        BufferedWriter BW = null;
        ServerSocket SS = null;
        try {
            SS = new ServerSocket(1234);    
            while(true) {
                    socket = SS.accept();
                    ISR = new InputStreamReader(socket.getInputStream());
                    OSW = new OutputStreamWriter(socket.getOutputStream());
                    BR = new BufferedReader(ISR);
                    BW = new BufferedWriter(OSW);

                    while(true) {
                        String command = BR.readLine();
                        System.out.println("Command: " + command);
                        if(command == null) 
                            BW.write("ERROR");
                        else if(command.equals("DATE")) 
                            BW.write(LocalDate.now().toString());
                        else if (command.equals("TIME"))
                            BW.write(LocalDateTime.now().toString());
                        else 
                            BW.write("ERROR");
                        BW.newLine();
                        BW.flush();
                    }
                }
            }
            catch(IOException e) {
                e.printStackTrace();
            }
            finally {
                try {
                    if(socket != null) socket.close();
                    if(ISR != null) ISR.close();
                    if(OSW != null) OSW.close();
                    if(BR != null) BR.close();
                    if(BW != null) BW.close();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
    }

    private static void connectToUDPServer() {
        InetAddress address = InetAddress.getLoopbackAddress();
        Scanner scanner = new Scanner(System.in);
        Integer port = 12000;
        DatagramSocket socket = null;
        try {
            socket = new DatagramSocket();
            while(true) {
                String message = scanner.nextLine();
                byte[] buf = message.getBytes();
                DatagramPacket packet = new DatagramPacket(buf, buf.length, address, port);
                socket.send(packet);
                byte[] receiverBuf = new byte[1024];
                packet = new DatagramPacket(receiverBuf, receiverBuf.length);
                socket.receive(packet);
                String received = new String(packet.getData(), 0, packet.getLength());
                System.out.println("Response: " + received);
            }
        } catch (SocketException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            if(scanner != null) scanner.close();
            if(socket != null) socket.close();
        }
    }

    private static void startUDPServer() {
        DatagramSocket socket = null;
        try {
            socket = new DatagramSocket(12000);
            System.out.println("Waiting for packets");
            while(true) {
                byte[] buf = new byte[8192];
                DatagramPacket packet = new DatagramPacket(buf, buf.length);
                socket.receive(packet);
                String command = new String(packet.getData(), 0, packet.getLength());
                System.out.println("Command: " + command);
                String responsePayload;
                if(command.equals("DATE")) 
                    responsePayload = LocalDate.now().toString();
                else if (command.equals("TIME"))
                    responsePayload= LocalDateTime.now().toString();
                else 
                    responsePayload = "ERROR";
                InetAddress address = packet.getAddress();
                int port = packet.getPort();
                buf = responsePayload.getBytes();
                packet = new DatagramPacket(buf, buf.length, address, port);
                socket.send(packet);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            if(socket != null) socket.close();
        }
    }
}