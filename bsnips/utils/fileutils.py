import os
import hashlib
import shutil

log = __import__("logging").getLogger(__name__)


def md5_hasher(path, blocksize=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


def get_file_stats(path):
    log.debug('Analyzing file %s' % path)
    stats = os.stat(path)
    h = md5_hasher(path)
    return path, h, stats


def stats_walk(path):
    for root, dirs, files in os.walk(path):
        log.debug('Scanning %s' % path)
        for f in files:
            yield get_file_stats(os.path.join(root, f))


def increment_file_number(dir_path, filename, count=1):
    """Based on existing files in dir_path increment the file count suffix"""
    if os.path.exists(os.path.join(dir_path, filename)):
        log.debug('{} already exists in {}'.format(filename, dir_path))
        name, ext = os.path.splitext(filename)
        name += '-{}'.format(count)
        new_filename = name + ext
        log.debug('Generated new name, "{}". Checking availability...'.format(new_filename))
        if os.path.exists(os.path.join(dir_path, new_filename)):
            return increment_file_number(dir_path, filename, count + 1)
        log.info('{} identified.'.format(new_filename))
        return new_filename
    log.info('{} identified.'.format(filename))
    return filename


def move_file(source, destination):
    log.debug('Moving "{}" to "{}".'.format(source, destination))
    return shutil.move(source, destination)


def move_delete(dir_path, filename):
    """Moves files into the special destination, dir_path. Normalizes file
    names to avoid conflict."""
    # Get path, name from filename
    path, name = os.path.split(filename)
    # Normalize with destination considerations
    nf = increment_file_number(dir_path, name)
    move_file(filename, nf)
