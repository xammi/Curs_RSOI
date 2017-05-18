CURRENT_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

function find_projects {
    local currentdir="${CURRENT_DIR}"

    for i in $(ls -1 $currentdir); do
        filepath=$currentdir/$i

        if [ -d $filepath ]; then

            if [ -e $filepath/Dockerfile ]; then
                docker build -t $i $filepath
            fi
        fi
    done
}

find_projects

