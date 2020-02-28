#!/usr/bin/env perl

if ($ARGV[0] eq "-r") {
    for (;;) {
        system("python3 ~/Документы/vkbots/python/chat/chatbot.py&");
        sleep(60 * 40);
    }
} else {
    system("python3 ~/Документы/vkbots/python/chat/chatbot.py");
}
