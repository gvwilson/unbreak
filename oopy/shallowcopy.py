import copy


class Playlist:
    def __init__(self, songs):
        self.songs = songs


original = Playlist(["alpha", "beta"])
# BUG: copy.copy is shallow — the new Playlist is a separate object, but its
# BUG: `songs` attribute still points at the same list, so appending to the
# BUG: copy mutates the original's list too
clone = copy.copy(original)
clone.songs.append("gamma")
print(original.songs)  # expect ['alpha', 'beta'], get ['alpha', 'beta', 'gamma']
