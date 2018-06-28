package sslperf;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.buffer.PooledByteBufAllocator;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.WriteBufferWaterMark;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;
import io.netty.handler.ssl.SslContext;
import io.netty.handler.ssl.SslContextBuilder;
import io.netty.handler.ssl.SslProvider;
import io.netty.handler.ssl.util.SelfSignedCertificate;


public class NettyServer {
    static final int PORT = Integer.parseInt(System.getProperty("port", "8992"));
    static String provider = System.getProperty("provider", "JDK");
    
    public static void main(String[] args) throws Exception {
        
        if(args.length >= 1) {
            provider = args[0];
        }
        System.out.println("Start server on "+ PORT + "  configured provider is "+ provider);
        SelfSignedCertificate ssc = new SelfSignedCertificate("127.0.0.1");
        SslContext sslCtx = SslContextBuilder.forServer(ssc.certificate(), ssc.privateKey())
        .sslProvider(SslProvider.valueOf(provider))
        .sessionCacheSize(1_000_000_000)
        .build();

        System.out.println("SSL Context: " + sslCtx.getClass());
        System.out.println("Cipher suites: ");
        for(String cipher : sslCtx.cipherSuites()) {
            System.out.println(cipher);
        }


        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        try {
            System.out.println("Binding...");
            ServerBootstrap b = new ServerBootstrap();

            b.option(ChannelOption.TCP_NODELAY, true);
            b.option(ChannelOption.SO_REUSEADDR, true);
            b.option(ChannelOption.SO_LINGER, 0);
            b.childOption(ChannelOption.TCP_NODELAY, true);
            b.childOption(ChannelOption.SO_REUSEADDR, true);
            b.childOption(ChannelOption.SO_KEEPALIVE, true);
            b.childOption(ChannelOption.SO_LINGER, 0);
            b.childOption(ChannelOption.SO_RCVBUF, 1048576);
            b.childOption(ChannelOption.SO_SNDBUF, 1048576);
            b.childOption(ChannelOption.WRITE_BUFFER_WATER_MARK, new WriteBufferWaterMark(2*65536, 10*65536));
            b.childOption(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT);

            b.group(bossGroup, workerGroup)
            .channel(NioServerSocketChannel.class)
            .handler(new LoggingHandler(LogLevel.INFO))
            .childHandler(new SecureChatServerInitializer(sslCtx));
            
            b.bind(PORT).sync().channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}