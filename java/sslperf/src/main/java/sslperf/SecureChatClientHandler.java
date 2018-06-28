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
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.channel.ChannelInboundHandlerAdapter;
import io.netty.util.AttributeKey;

/**
 * Handles a client-side channel.
 */
public class SecureChatClientHandler extends ChannelInboundHandlerAdapter {

    volatile long lengthTarget = 0;
    long requestSendOutTime = 0;
    long received = 0;

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        System.out.println("Reading...  "+ System.currentTimeMillis() + " : " + lengthTarget);

        ByteBuf buf = (ByteBuf)msg;
        long currentReceivedTime = System.nanoTime();
        long rlength = buf.readableBytes();
        received += rlength;

        if ( received % lengthTarget == 0 ) {
            System.out.println("Speed = " + (received * 1000 ) / (currentReceivedTime - requestSendOutTime));
        }
        buf.release();
//        System.out.println(String.format("%s  -  %s , total received %s", currentReceivedTime, lastReceivedTime, received));
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
