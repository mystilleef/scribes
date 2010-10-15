def get_selected_path(treeview):
	#FIXME: This function is deprecated.
	model, iterator = treeview.get_selection().get_selected()
	if not iterator: return None
	return model.get_path(iterator)

def get_selected_paths(treeview):
	return treeview.get_selection().get_selected_rows()[-1]
