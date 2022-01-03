from foxy.listener.event import Event

# Api events

# Cell events
class CellEvent(Event): pass

class onCellCreate(CellEvent): pass
class onCellChange(CellEvent): pass
class onCellGet(CellEvent): pass
class onCellDelete(CellEvent): pass

# Table events

# database events