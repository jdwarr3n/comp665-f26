"""
Convert matplotlib objects to dictionary form

Follows spec given in mpl_dict_spec.txt
"""

ADD_DEFAULTS = False

def round_list(numbers, digits=3):
    """
    Input: list numbers, int digits
    
    Output: list with numbers rounded to specified number of digits
    """
    return [round(num, digits) for num in numbers]

def obj_to_dict(obj):
    """
    Input: matplotlib object obj
    
    Output: dictionary equivalent of obj
    """
    
    ans = {}
    def add_attribute(attribute, val, default_val):
        if (val != default_val) or ADD_DEFAULTS:
            ans[attribute] = val
    
    obj_name = type(obj).__name__
    if obj_name == "Figure":
        ans["subplots"] = [obj_to_dict(subplot) for subplot in obj.get_axes()]
        add_attribute("suptitle", obj_to_dict(obj._suptitle), None)
        #add_attribute("dpi", obj.get_dpi(), 100.0)
        #add_attribute("size_inches", list(obj.get_size_inches()), [6.4, 4.8])
        add_attribute("dpi", obj.get_dpi(), 72.0)
        add_attribute("size_inches", list(obj.get_size_inches()), [6.0, 4.0])
        return ans
    
    elif obj_name == "AxesSubplot":
        
        # Formatting
        ans["row"] = obj.rowNum
        ans["col"] = obj.colNum
        add_attribute("title", obj_to_dict(obj.title), None)

        # Guides
        if obj.axison:
            ans["xaxis"] = obj_to_dict(obj.get_xaxis())
            ans["yaxis"] = obj_to_dict(obj.get_yaxis())        
        add_attribute("legend", obj_to_dict(obj.get_legend()), None)

        # Graphical objects
        add_attribute("lines", [obj_to_dict(line) for line in obj.lines], [])
        add_attribute("collections", [obj_to_dict(collection) for collection in obj.collections], [])
        add_attribute("images", [obj_to_dict(image) for image in obj.images], [])
        add_attribute("patches", [obj_to_dict(patch) for patch in obj.patches], [])
        add_attribute("texts", [obj_to_dict(text) for text in obj.texts], [])
        return ans
    
    elif obj_name in set(["XAxis", "YAxis"]):
        ans["ticklabels"] = [label.get_text() for label in obj.get_ticklabels()]
        ans["ticklocs"] = round_list(obj.get_ticklocs())
        add_attribute("label", obj_to_dict(obj.get_label()), None)
        return ans
    
    elif obj_name == "Legend":
        ans["position"] = obj._loc_real
        ans["handles"] = [obj_to_dict(handle) for handle in obj.get_lines()]  # Labeled lines only
        ans["labels"] = [obj_to_dict(label) for label in obj.get_texts()]
        add_attribute("title", obj_to_dict(obj.get_title()), None)
        return ans
    
    elif obj_name == "Text":
        txt = obj.get_text()
        if txt == "":
            return None
        ans["text"] = txt
        
        # use obj.get_transform() to convert all text positions to figure coordinates
        fig = obj.get_figure()
        display_pos = obj.get_transform().transform(obj.get_position())
        fig_pos = fig.transFigure.inverted().transform(display_pos)
        ans["position"] = round_list(fig_pos)
        
        add_attribute("color", obj.get_color(), "black")
        add_attribute("fontsize", obj.get_fontsize(), 10.0)
        add_attribute("fontname", obj.get_fontname(), "DejaVu Sans")
        add_attribute("fontstyle", obj.get_fontstyle(), "normal")
        return ans
        
    elif obj_name == "Line2D":
        ans["linecolor"] = obj.get_color()
        ans["xdata"] = round_list(obj.get_xdata())
        ans["ydata"] = round_list(obj.get_ydata())
        add_attribute("linestyle", obj.get_linestyle(), "-") 
        #add_attribute("marker", obj.get_marker(), "None")
        return ans
    elif obj_name == "AxesImage":
        extent = obj.get_extent()
        ans["size"] = [extent[1] - extent[0], extent[2] - extent[3]]
        ans["position"] = [extent[0], extent[3]]
        ans["array"] = obj.get_array().tolist()
        ans["colormap"] = obj.get_cmap()
        return ans 
    elif obj_name in set(["Rectangle", "Polygon", "RegularPolygon", "CirclePolygon"]):
        ans["type"] = obj_name
        ans["size"] = [obj.get_width(), obj.get_height()]
        ans["position"] = list(obj.get_xy())
        ans["facecolor"] = round_list(obj.get_facecolor())
        add_attribute("edgecolor", round_list(obj.get_edgecolor()), [0, 0, 0, 0])
        return ans
    elif obj_name in set(["PathCollection"]):
        ans["type"] = "path"
        ans["sizes"] = obj.get_sizes().tolist()
        ans["positions"] = obj.get_offsets().tolist()
        ans["colors"] = obj._facecolors.tolist()
        return ans   
    
    else:
        #print("Unsupported matplotlib object type", obj_name)
        return obj
        
    
    