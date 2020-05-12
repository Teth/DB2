#!/bin/bash
redis-server
python demo_journal.py &
sleep 0.5
python demo_worker_launch.py &
python demo_mock_client.py demouser 10 &