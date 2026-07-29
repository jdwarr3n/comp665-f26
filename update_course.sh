#!/bin/bash
# Pull the latest course updates (checkers, scripts, templates) into your
# copy of the repo:
#     ./update_course.sh
# Safe to run any time. Commit your own work first if you have unsaved
# changes; if the merge reports a conflict, commit your work and ask the
# instructor.
#
# Points at the official course starter repo below.

COURSE_REPO="https://github.com/jdwarr3n/comp665-starter"

git remote add upstream "$COURSE_REPO" 2>/dev/null
git remote set-url upstream "$COURSE_REPO"
git fetch upstream || exit 1
# --allow-unrelated-histories: template copies start with their own initial
# commit; needed on the first merge only, harmless after that.
git merge upstream/main --allow-unrelated-histories -m "Course update" || {
    echo
    echo "The update did not merge cleanly. Commit your work, then ask the instructor."
    exit 1
}
echo
echo "Course files are up to date."
