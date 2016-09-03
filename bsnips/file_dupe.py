import os, datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from utils.fileutils import stats_walk, move_delete

log = __import__("logging").getLogger(__name__)
DB_NAME = 'file_dupe.sqlite'
db = SqliteExtDatabase(DB_NAME)


def setup():
    if os.path.exists(DB_NAME):
        log.debug('Removing database file before setup')
        os.remove(DB_NAME)
    # Connect to the database and create tables
    global db
    db.connect()
    db.create_tables([File])


def destroy():
    global db
    if db is not None:
        db.close()
    if os.path.exists(DB_NAME):
        log.debug('Removing database file on finishing.')
        os.remove(DB_NAME)


def create_delete_folder(path):
    d = os.path.join(path, 'Deleted')
    if not os.path.exists(d):
        os.mkdir(d)
    return d


class BaseModel(Model):
    class Meta:
        database = db


class File(BaseModel):
    path = CharField(unique=True, primary_key=True)
    short_name = CharField()
    size = IntegerField(index=True)
    last_mod_time = DateTimeField()
    created_time = DateTimeField(index=True)  # windows system
    hash_digest = CharField(index=True)
    exists = BooleanField(default=True)
    has_duplicate = BooleanField(default=False)


def search(path):
    """Save stats to database"""
    global db
    with db.atomic():
        for p, digest, stats in stats_walk(path):
            f = File.create(
                path=p, short_name=os.path.split(p)[1], size=stats.st_size,
                last_mod_time=datetime.datetime.fromtimestamp(stats.st_mtime),
                created_time=datetime.datetime.fromtimestamp(stats.st_ctime),
                hash_digest=digest,
            )
            # check if duplicate exists
            # log.debug('Checking for duplicates')
            # x = find_duplicates_now(f)
            # log.info('Updated %d matches for %s' % (x, f.short_name))


def find_duplicates():
    """Duplicates are identified by size, date_modified and content"""
    # Identifies all duplicates in one pass after the scan rather than during it
    log.debug('Checking for duplicates')
    FileAlias = File.alias()
    # Subquery getting the total number of files with matching attributes
    sq = (
        FileAlias
            .select(fn.COUNT(FileAlias.path))
            .where(FileAlias.size == File.size,
                   FileAlias.hash_digest == File.hash_digest
                   )
    )

    # Wrap the subquery and filter on the count.
    query = (File.update(has_duplicate=True).where(sq > 1))
    num_duplicates = query.execute()
    log.info('Found {} duplicates in total'.format(num_duplicates))
    return num_duplicates


def find_duplicates_now(f):
    """Duplicates are identified by size, date_modified and content"""
    # Create sqlite database. (There may be to much data to hold in memory. Allows resuming presumably)
    # Crawl the given path adding file details to the database
    # Identify duplicates by matching against stored data

    files = File.select().where(
        File.size == f.size, File.hash_digest == f.hash_digest
    ).count()
    log.info('Found %d matches for %s' % (files, f.short_name))
    if files > 1:
        query = File.update(has_duplicate=True).where(
            File.size == f.size, File.hash_digest == f.hash_digest
        )
        return query.execute()
    return 0


def handle_duplicates(path, confirm_delete=False):
    """Duplicates may be deleted or moved. The oldest version of the file is kept."""
    files = (
        File
            .select()
            .where(File.has_duplicate == True)
            .order_by(File.created_time)
            .group_by(File.hash_digest))
    files = (
        File
            .select()
            .where(File.has_duplicate == True, ~(File.path << files))
    )
    log.info('{} files are going to be deleted'.format(files.count()))
    if not confirm_delete:
        for f in files:
            log.info('Moving "{}". Was created on {} & last modified on {}.'.format(
                f.short_name, f.created_time, f.last_mod_time
            ))
            # move files to a special folder
            move_delete(create_delete_folder(path), f.path)
    if confirm_delete:
        for f in files:
            log.info('Deleting "{}". Was created on {} & last modified on {}.'.format(
                f.short_name, f.created_time, f.last_mod_time
            ))
            os.remove(f.path)


def main():
    setup()
    prompt = raw_input("Please enter file path to be scanned:")
    try:
        if prompt and not os.path.exists(prompt):
            raise ValueError('{} does not exist'.format(prompt))
    except ValueError as e:
        log.exception(e)
        prompt = os.getcwd()
    search(prompt)
    dup_count = find_duplicates()
    if dup_count:
        handle_duplicates(prompt)
    destroy()


if __name__ == '__main__':
    from utils.log import setup_logging

    setup_logging(20)
    main()
