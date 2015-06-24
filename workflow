#!/bin/bash

while [ ! $# -eq 0 ]; do
    case $1 in
        "-s")
            SUITE="$2"; shift 2
            ;;
        "-w")
            WORKER="$2"; shift 2
            ;;
        "-t")
            EXPECT="$2"; shift 2
            ;;
        "-m")
            MODULE="$2"; shift 2
            ;;
        *)
            echo "Bad arguemnt"; exit 1
            ;;
    esac
done

: ${SUITE:?"Need to specify test suite"}
: ${WORKER:?"Need to specify worker number"}
: ${EXPECT:?"Need to specify time before graceful exit"}
: ${MODULE:?"Need to specify which module in test suite"}

## Launch the test suite
CID=$(
docker run -d --link bigobject:bigobject \
    -e BIGOBJECT_HOST=bigobject \
    -e WORKER=${WORKER} \
    macrodata/integration-test:${SUITE} \
    python -c "from cmd.${MODULE} import work; import run; run.main(work)"
)

cleanup() {
	docker logs ${CID}
	docker rm -f ${CID} &>/dev/null
}

waitforit() {
	trap "exit 0" SIGTERM
	# wait for aribitrary time before reaping
	RET=$(docker wait ${CID})
	exit ${RET}
}

alarm() {
	PID=${1:?"No pid specified"}
	sleep ${EXPECT}
	kill -TERM ${PID}
}

# capture exit status of test
waitforit & WPID=$!

# gracefully stop after sometime
alarm ${WPID} & APID=$!

wait ${WPID}
RET=$?

kill -9 ${APID} &>/dev/null
trap - SIGTERM
cleanup

exit ${RET}
