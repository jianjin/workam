/*
 * Copyright 2012 The Netty Project
 *
 * The Netty Project licenses this file to you under the Apache License,
 * version 2.0 (the "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */
package sslperf;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.PooledByteBufAllocator;
import io.netty.buffer.Unpooled;
import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelOutboundHandler;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.handler.ssl.SslHandler;
import io.netty.util.concurrent.Future;
import io.netty.util.concurrent.GenericFutureListener;
import io.netty.util.concurrent.GlobalEventExecutor;
import io.netty.channel.ChannelInboundHandlerAdapter;

import java.net.InetAddress;

/**
 * Handles a server-side channel.
 */
public class SecureFile extends ChannelInboundHandlerAdapter{

    static final ChannelGroup channels = new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);
    static final ByteBuf data = Unpooled.buffer(10_000_000);
    static {
        System.out.println("Initializing data for writing, Capacity is:" + data.capacity());
        for(int i = 0 ; i < data.capacity(); i++){
            data.writeByte(1);
        }
        System.out.println(data);
    }

    @Override
    public void channelActive(final ChannelHandlerContext ctx) {
        // Once session is secured, send a greeting and register the channel to the global channel
        // list so the channel received the messages from others.
        ctx.pipeline().get(SslHandler.class).handshakeFuture().addListener(
                new GenericFutureListener<Future<Channel>>() {
                    @Override
                    public void operationComplete(Future<Channel> future) throws Exception {
                        System.out.println("Your session is protected by " +
                                ctx.pipeline().get(SslHandler.class).engine().getSession().getCipherSuite() +
                                " cipher suite.\n");
                        ctx.writeAndFlush(
                                "Welcome to " + InetAddress.getLocalHost().getHostName() + " secure chat service!\n");
                        ctx.writeAndFlush(
                                "Your session is protected by " +
                                        ctx.pipeline().get(SslHandler.class).engine().getSession().getCipherSuite() +
                                        " cipher suite.\n");

                        channels.add(ctx.channel());
                    }
                });
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        System.out.println("Read Task Started: " + System.currentTimeMillis() + " " + msg);
        System.out.println("Writing..");
        int length = 10_000_000;
        try {
            length = Integer.parseInt((String)msg);
        } catch (NumberFormatException e){
            System.err.println(e.getMessage());
        }
        long start = System.nanoTime();
        for(int i = 0 ; i < 100 ; i++) {
            ByteBuf bb = data.slice(0, length < 10_000_000 ? length : 10_000_000);
            bb.writerIndex(bb.capacity());
//            System.out.println("Writing " + System.currentTimeMillis() + " : " + bb);
            ctx.writeAndFlush(bb.retain());
//            System.out.println("Writing completed " + System.currentTimeMillis() + " : " + bb);
        }
        long end = System.nanoTime();
        System.out.println("Speed on the server side: " + (long)length * 100 * 1000 / (end - start));
    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) {
        ctx.flush();
        System.out.println("Read task completed @"+ System.currentTimeMillis());
    }


    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
