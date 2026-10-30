#!/bin/zsh
# A18: role-v51 (main_driver's product branch as the page's §3 B row, with one example and one counter-example) beside a simultaneous
# role-v42 on the five small-product articles and the fifteen articles whose gold holds a main-product question, six draws.
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
W=/Users/lchingen/hivemind-extraction-quality-2026-10-28
IDS=(gnews:2c6a829280cba26d8c8adf60 nvblog:geforce-now-thursday-toronto-expansion gnews:cafa45974d83b062f52155e9 gnews:9026c944c63575a080ce7ba9 gnews:c638ce9c979628354cec3fbb gnews:af6e4910e877d5682a773d4b gnews:2f953a56cd06571ab0afc348 gnews:552f8c2bdfd080555d592587 gnews:68a3ed21f77b935d9fa7ec5e gnews:98a4e8ff0c0260d8dc9e531d gnews:f66e1689ec2e27e7eab2a2dd gnews:795ea94e1100415a67fd1a96 gnews:d5c48abb470f394f86549b6b gnews:d4c5dc540392f8df39aee250 gnews:c0432377817a1c00a1bbadf0 gnews:c75f16a6d64cc27fc28fb571 gnews:b48593184704bbbe6eddbc03 gnews:295fceb25273abae9bb6c995 gnews:c8c39f971721fd820aab5c1c gnews:57de52b4f33b0c903d256f9e)
for d in 1 2 3 4 5 6; do
  PYTHONPATH=$W/src:$W/poc:$PWD python3 loop.py send c18-v42-d$d $W/poc/config/poc-v58.json $IDS &
  PYTHONPATH=$W/src:$W/poc:$PWD python3 loop.py send c18-v51-d$d $W/poc/config/poc-v67.json $IDS &
  wait
done
echo A18-DONE
