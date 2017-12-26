﻿# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#  
#  Copyright 2015 Shai Seger <shaise at gmail dot com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################

class EnclosureWorkbench (Workbench):
 
    MenuText = "Electronics Enclosure"
    ToolTip = "Electronics enclosure generator"
    Icon = '''
/* XPM */
static char * C:\Users\mmayg\Pictures\encicon_xpm[] = {
"32 32 15 1",
" 	c None",
".	c #01188C",
"+	c #10B7F9",
"@	c #0FB7FA",
"#	c #0ED2F6",
"$	c #0FB6FA",
"%	c #000406",
"&	c #0ECFF7",
"*	c #0DCFF6",
"=	c #0ED0F6",
"-	c #0ECCF7",
";	c #10B7FA",
">	c #0ECFF6",
",	c #0DD0F6",
"'	c #0ED0F7",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"       .....................    ",
"      .+++++++++++++++++++..    ",
"     .+++++++++++++++++++.+.    ",
"    .+++++++++++++++++++.@+.    ",
"   .....................+++.    ",
"   .###################.+$+.    ",
"   .###################.+++.    ",
"   .####%%#####%%#####&.+++.    ",
"   .####%%###%%%%#####*.+++.    ",
"   .####%%#%%%%%%#####=.+++.    ",
"   .##%%%%%%%%%%%%%%%-&.+;+.    ",
"   .####%%#%%%%%%#####*.+;+.    ",
"   .####%%###%%%%#####>.+;+.    ",
"   .####%%#####%%#####&.++.     ",
"   .##################,.+.      ",
"   .##################'..       ",
"   .....................        ",
"                                ",
"                                ",
"                                ",
"                                "};
''' 
    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import DIYEnclosure
	self.appendToolbar("Enclosures", ["DIYEnclosure"])
	self.appendMenu("Enclosures", ["DIYEnclosure"])
	Log ("Loading MyModule... done\n")
        
 
    def Activated(self):
        "This function is executed when the workbench is activated"
        return
 
    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return
 
    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu
 
    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
 
Gui.addWorkbench(EnclosureWorkbench())