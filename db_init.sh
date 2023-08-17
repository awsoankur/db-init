while getopts "dp" flag; do
    case $flag in
    d) # Handle the -h flag
    # Display script help information
        if python db_start_test.py; then
            echo "Database Up and cleaned";
        else
            echo ;
            echo "Failed to estabilish proper connection with db";
            exit 1;
        fi
    ;;
    p) # Handle the -v flag
    # Enable verbose mode
        if alembic upgrade head; then
            echo "Database is up to date, filling in data"
        else
            echo ;
            echo "Some db migrations failed";
            exit 1;
        fi

        if python sync_models.py; then
            echo "Models are synced"
        else
            echo;
            echo "Modifications need to be made in 'db_params.py'";
            exit 1;
        fi

        if python db_fill.py then ; then
            echo "Database filled";
        else
            echo ;
            echo "Error while filling db";
            exit 1;
        fi
    ;;
 esac
done
