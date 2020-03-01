#!/usr/bin/env perl

sub main {
    my $par = shift;
    for (;;) {
        system("python3 ~/Документы/vkbots/python/chat/chatbot.py");
        last if ($par ne "r");
    }
    return 0;
}

exit(main(@ARGV));
