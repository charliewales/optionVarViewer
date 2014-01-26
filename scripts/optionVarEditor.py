import pymel.core as pm


class UI(object):
    def __init__(self):
        if pm.window('optionVarEditor', exists=True):
            pm.deleteUI('optionVarEditor')

        with pm.window(title='optionVarEditor', widthHeight=(502, 552), s=False) as window:
            with pm.columnLayout():
                with pm.rowColumnLayout(nc=2, cw=[(1, 250), (2, 250)]):
                    # List Column
                    with pm.columnLayout():
                        self.search = pm.textField(width=248, cc=self.refresh, ec=self.refresh)
                        self.scrollList = pm.textScrollList(height=500, width=250, selectCommand=self._select, ams=True)
                    # Attr Column
                    with pm.columnLayout():
                        pm.text(l='optionVar Name:')
                        self.name = pm.textField(tx='Name', ed=False, width=248)
                        pm.text(l='optionVar Value:')
                        self.value = pm.textField(tx='value', width=248)
                # Buttons
                with pm.rowColumnLayout(nc=3, cw=[(1, 166), (2, 166), (3, 166)]):
                    pm.button(label='Create', c=self._create)
                    pm.button(label='Edit', c=self._edit)
                    pm.button(label='Delete', c=self._delete)

        self.refresh()

        # Render Window
        window.show()

    def _select(self):
        self.sel = self.scrollList.getSelectItem()
        if len(self.sel) == 1:
            self.name.setText(self.sel[0])
            self.value.setText(pm.optionVar[self.sel[0]])
        else:
            self.name.setText('<Multiple Values>')
            self.value.setText('<Multiple Values>')

    def _create(self, *args):
        dialog(self)

    def _edit(self, *args):
        if len(self.sel) == 1:
            pm.optionVar[self.name.getText()] = self.value.getText()
            self.refresh()
        else:
            pm.warning('Can only edit 1 value at a time!')

    def _delete(self, *args):
        for i in self.sel:
            pm.optionVar.pop(i)
        self.refresh()

    def refresh(self, *args):
        self.scrollList.removeAll()
        for key in pm.optionVar:
            if self.search.getText() in key:
                self.scrollList.append(key)


class dialog(object):
    def __init__(self, mainUI):
        self.mainUI = mainUI
        with pm.window(title='Create') as self.window:
            with pm.columnLayout():
                self.name = pm.textFieldGrp(label='Name:')
                self.value = pm.textFieldGrp(label='Value:')

                with pm.rowColumnLayout(nc=2):
                    pm.button(label='create', c=self._apply)
                    pm.button(label='Cancel', c=self._cancel)

        self.window.show()

    def _apply(self, *args):
        pm.optionVar[self.name.getText()] = self.value.getText()
        self.mainUI.refresh()
        self.window.delete()

    def _cancel(self, *args):
        self.window.delete()
