CURRENT_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
PROJECTS=()

function find_projects {
    local currentdir="${CURRENT_DIR}"

    for i in $(ls -1 $currentdir); do
        filepath=$currentdir/$i

        if [ -d $filepath ]; then

            if [ -e $filepath/Dockerfile ]; then
                docker build -t $i $filepath
                docker stop $(docker ps -a | grep "${i}" | awk '{print $1}')
                PROJECTS+=($i)
            fi
        fi
    done
}

find_projects

if [ -z ${PROJECTS} ]; then
    echo "Projects not found"
else
	echo "Projects found: ${PROJECTS[@]}"
	
	echo "Deleting old images ..."
	docker rm $(docker ps -a -f status=exited -q)

	port=8000
	for i in ${PROJECTS}; do
		echo "Image starting: ${i} at port=${port} ..."
		docker run -p ${port}:80 -td ${i}
		port=$[port + 1]
	done
	echo "Successfully deployed"
fi
