# WORKSPACE INITIAL CONFIGURATION

# ścieżki ************************************************************************
workspace_path = r"Project1\workspace.gdb"

gminy_prg_path = r"Project1\dane\02_GraniceAdministracyjne\A03_Granice_gmin.shp"
gmina_name = "Świeradów-Zdrój"; gmina_name_field = "JPT_NAZWA_"

bdot_folders_paths_list = [r"Project1\dane\0210_SHP", r"Project1\dane\0212_SHP"]

out_shp_krawedzie = r"Project1\dane\aGraf\krawedzie.shp"
out_shp_start_nd = r"Project1\dane\aGraf\wezly_start.shp"

# !                 ______________________________________________________________
distance = 10200    # jak daleko szukać węzłów (m)
# !                 ______________________________________________________________

# ********************************************************************************

import arcpy

arcpy.env.workspace = workspace_path
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("ETRF2000-PL CS92")
arcpy.env.cellSize = 5
arcpy.env.overwriteOutput = True

# ciężkie drogi
import os
from pathlib import Path

if __name__ == "__main__":
    l_skdr = [] 
    # get shapefiles
    bdot_folders = bdot_folders_paths_list
    for folder in bdot_folders:
        # rename bad filenames
        file_list = [str(file) for file in Path(folder).rglob('*')]
        for filename_bad in file_list:
            filename = ""
            for i, ch in enumerate(filename_bad):
                if ch == "." and i < len(filename_bad) - 5:
                    filename += '_'
                else:
                    filename += ch
        
            os.rename(filename_bad, filename)
            
            # filename = filename.replace("\\", "\\\\")
            if filename.endswith(".shp"):
                if "OT_SKDR_L" in filename:
                    l_skdr.append(filename)

    # merge layer
    arcpy.management.Merge(l_skdr, "powiatySKDR_L")

    # *********************************************
    # drogi
    filter = "KAT_ZARZAD IN ('krajowa', 'wojewódzka', 'powiatowa', 'gminna') AND MATE_NAWIE IN ('beton', 'kostka kamienna', 'kostka prefabrykowana', 'masa bitumiczna', 'płyty betonowe', 'żwir', 'tłuczeń')"
    powiatyKrawedzieSiec = arcpy.management.SelectLayerByAttribute('powiatySKDR_L', "NEW_SELECTION", filter)
    arcpy.management.CopyFeatures(powiatyKrawedzieSiec, out_shp_krawedzie)

    # węzły
    filter2 = "KAT_ZARZAD IN ('krajowa', 'wojewódzka')"
    powiatyDrogiMiedzyWezlami = arcpy.management.SelectLayerByAttribute('powiatySKDR_L', "NEW_SELECTION", filter2)
    arcpy.management.CopyFeatures(powiatyDrogiMiedzyWezlami, 'powiatyDrogiMiedzyWezlami')

    arcpy.analysis.Intersect(['powiatyDrogiMiedzyWezlami'], 'powiatyWezlyWielokrotne', "", "", "point")
    arcpy.analysis.CountOverlappingFeatures(
        in_features="powiatyWezlyWielokrotne",
        out_feature_class="powiatyWezlyMultipart",
        min_overlap_count=3,
        out_overlap_table=None
    )

    # multipart to singlepart
    arcpy.management.MultipartToSinglepart("powiatyWezlyMultipart", "powiatyWezlySinglepart")

    # *********************************************
    # getting the gmina shape
    gmina = gmina_name; gmina_field = gmina_name_field
    gminy_file = gminy_prg_path
    with arcpy.da.SearchCursor(gminy_file, [gmina_field, "SHAPE@"]) as cursor:
        for row in cursor:
            random_gmina_from_file = row[0]
            if random_gmina_from_file == gmina:
                arcpy.CopyFeatures_management(row[1], "gmina_sam")

    # buffer defining the area of looking for the start nodes
    arcpy.analysis.Buffer("gmina_sam", "gminaStartNodesBuff", f"{distance} Meters")

    # intersect
    close_nodes = arcpy.management.SelectLayerByLocation("powiatyWezlySinglepart", "INTERSECT", "gminaStartNodesBuff", selection_type="NEW_SELECTION")
    arcpy.management.CopyFeatures(close_nodes, out_shp_start_nd)
