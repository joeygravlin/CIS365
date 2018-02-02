.PHONY: model_short_training model_long_training clean_model clean_data default data

# First-Place bot for Halite2 - let's train our bot to act like them!
USER_NAME=reCurs3
USER_ID=1896
MAX_NUM_REPLAY_FILES=2018
DEST_DIR=${USER_NAME}-${USER_ID}-replays
# Name of the data file
FILE=${DEST_DIR}.zip

# Halite binary address - please change here if you're not using MacOS
HALITE_BINARY_ADDRESS=https://halite.io/assets/downloads/Halite2_Linux-x64.zip

# There is nothing special about this seed (other that it's the 1 milionth prime) .
SEED=15485863

SOURCES_FOR_TRAINING= tsmlstarterbot/common.py \
	tsmlstarterbot/neural_net.py tsmlstarterbot/parsing.py \
	tsmlstarterbot/train.py

default: model_long_training

model_long_training_self: models/model_long_training_self.ckpt.meta

model_long_training: models/model_long_training.ckpt.meta

model_short_training: models/model_short_training.ckpt.meta

models/model_long_training_self.ckpt.meta: data/${FILE} ${SOURCES_FOR_TRAINING}
	mkdir -p models/
	# Needs more work, probably want to serially export the replay data...
	python3 -m tsmlstarterbot.train --model_name model_long_training_self --data data/${FILE} --games_limit ${MAX_NUM_REPLAY_FILES} --steps 5000 

models/model_long_training.ckpt.meta: data/${FILE} ${SOURCES_FOR_TRAINING}
	mkdir -p models/
	python3 -m tsmlstarterbot.train --model_name model_long_training --data data/${FILE} --games_limit ${MAX_NUM_REPLAY_FILES} --steps 5000 --seed ${SEED}
	# python3 -m tsmlstarterbot.train --model_name model_long_training --data data/${FILE} --games_limit ${MAX_NUM_REPLAY_FILES} --steps 5000 --seed ${SEED} --bot_to_imitate ${USER_NAME}

models/model_short_training.ckpt.meta: data/${FILE} ${SOURCES_FOR_TRAINING}
	mkdir -p models/
	python3 -m tsmlstarterbot.train --model_name model_short_training --data data/${FILE} --games_limit 100 --steps 500 --seed ${SEED}

clean_model:
	rm -rf models

clean_data:
	rm -rf data

clean_tarball:
	rm -rf ${SUBMISSION_TARBALL_DIR}

real_clean: clean_model clean_data
	rm -f submission.zip
	rm -f bin/halite

data: data/${FILE}

REPLAY_FILES := $(wildcard data/${DEST_DIR}/*)
NUM_REPLAY_FILES := $(words ${REPLAY_FILES})

data/${FILE}:
	mkdir -p data/${DEST_DIR}
ifeq (${NUM_REPLAY_FILES},${MAX_NUM_REPLAY_FILES})
	@echo NUM_REPLAY_FILES: ${NUM_REPLAY_FILES}
else
	@echo MAX_NUM_REPLAY_FILES: ${MAX_NUM_REPLAY_FILES}
	@echo NUM_REPLAY_FILES: ${NUM_REPLAY_FILES}
	hlt replay user -i ${USER_ID} -l ${MAX_NUM_REPLAY_FILES} -d data/${DEST_DIR}
	# https://halite.io/learn-programming-challenge/halite-cli-and-tools/halite-client-tools
	zip -rj  data/${FILE}  data/${DEST_DIR}/*
endif


CLASS_BOTS_DIR :=../halite_bots
CLASS_BOTS := $(wildcard ${CLASS_BOTS_DIR}/*)
#NUM_CLASS_BOTS := $(words ${CLASS_BOTS})

GYM_PLAYER_1 :="python3 MyBot.py"
#GYM_PLAYER_2 ="python3 ${CLASS_BOTS_DIR}/${CLASS_BOTS}"

GYM_ITERATIONS =50
GYM_HEIGHT =240
GYM_WIDTH =160

# This is a dirty use of BASH scripting in a Makefile... Should just make a permutation script in python...
gym_class: bin/halite
	for GYM_PLAYER_2 in ${CLASS_BOTS_DIR}/* ; do \
	  hlt gym \
	  -r ${GYM_PLAYER_1} \
	  -r "python3 $${GYM_PLAYER_2}" \
	  -b "bin/halite" \
	  -i ${GYM_ITERATIONS} \
	  -H ${GYM_HEIGHT} \
	  -W ${GYM_WIDTH} ; \
	done ; 

GYM_REPLAY_DIR :=../halite_bots_replays
# This is a dirty use of BASH scripting in a Makefile... Should just make a permutation script in python...
gym_class_replays: bin/halite
	mkdir -p ${GYM_REPLAY_DIR}
	for GYM_PLAYER_2 in ${CLASS_BOTS_DIR}/* ; do \
	  bin/halite \
	  -d "${GYM_HEIGHT} ${GYM_WIDTH}" \
	  --seed ${SEED} \
	  --replaydirectory ${GYM_REPLAY_DIR} \
	  ${GYM_PLAYER_1} \
	  "python3 $${GYM_PLAYER_2}" ; \
	done ; 

GYM_SELF_REPLAY_DIR :=self_replays
gym_self_replays: bin/halite
	mkdir -p ${GYM_SELF_REPLAY_DIR}
	bin/halite \
	-d "${GYM_HEIGHT} ${GYM_WIDTH}" \
	--seed ${SEED} \
	--replaydirectory ${GYM_SELF_REPLAY_DIR} \
	${GYM_PLAYER_1} \
	${GYM_PLAYER_1} ;

bin/halite:
	curl -C - $(HALITE_BINARY_ADDRESS) -o halite_binary.zip
	unzip halite_binary.zip -d bin
	rm -rf halite_binary.zip

compare: bin/compare.sh MyBotShortTraining.py MyBot.py model_short_training model_long_training bin/halite
	bin/compare.sh MyBotShortTraining.py MyBot.py

submission: 
	zip -r submission.zip MyBot.py LANGUAGE hlt/ tsmlstarterbot/ models/

TEAMNAME:=DELorousTRON3030
SUBMISSION_TARBALL_DIR:=cis365_project01_-_${TEAMNAME}
submission_tarball:
	mkdir -p ${SUBMISSION_TARBALL_DIR}
	rsync -ChavP  Makefile README* WRITEUP* MyBot.py LANGUAGE hlt tsmlstarterbot models ${SUBMISSION_TARBALL_DIR}
	mv ${SUBMISSION_TARBALL_DIR}/MyBot.py ${SUBMISSION_TARBALL_DIR}/${TEAMNAME}_final_bot.py
	chmod -R +X ${SUBMISSION_TARBALL_DIR}
	chmod -R ugo+r ${SUBMISSION_TARBALL_DIR}
	#find ${SUBMISSION_TARBALL_DIR}/. -type d -name \* -exec chmod 775 {} \;
	tar -cvzf ${SUBMISSION_TARBALL_DIR}.tar.gz ${SUBMISSION_TARBALL_DIR}
	chmod -R ugo+r ${SUBMISSION_TARBALL_DIR}.tar.gz


