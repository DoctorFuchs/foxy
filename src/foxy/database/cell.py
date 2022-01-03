from foxy.utils.publisher import Public
from foxy.utils.property_manager import generate_property_with_events
from foxy.listener.database import onCellChange, onCellGet, onCellDelete, onCellCreate

class Cell:
    def __init__(self, pos, value="", raw_value="") -> None:
        onCellCreate(cancelable=False)(Public(self))
        self.value = value
        self.raw_value = raw_value
        self.pos = pos

        self.value = generate_property_with_events("value", onCellGet(cancelable=False), onCellChange(), onCellDelete())
        self.raw_value = generate_property_with_events("raw_value", onCellGet(cancelable=False), onCellChange(), onCellDelete())
        self.pos = generate_property_with_events("pos", onCellGet(cancelable=False), onCellChange(), onCellDelete())

    def _add_to_table(self, table):
        table._add_cell(self)