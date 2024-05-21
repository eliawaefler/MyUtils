import ifcopenshell


def load_ifc(file_path):
    """ Lädt eine IFC-Datei und gibt das Modell zurück. """
    return ifcopenshell.open(file_path)


def extract_structure(ifc_model):
    """ Extrahiert relevante Strukturen und Daten aus einem IFC-Modell. """
    elements = {}
    for element in ifc_model.by_type('IfcProduct'):
        element_type = element.is_a()
        if element_type not in elements:
            elements[element_type] = []
        elements[element_type].append(element)
    return elements


def compare_ifc_models(model1, model2):
    """ Vergleicht zwei IFC-Modelle auf ihre Ähnlichkeit basierend auf ihrer Struktur. """
    structure1 = extract_structure(model1)
    structure2 = extract_structure(model2)
    
    # Ähnlichkeit basierend auf der Anzahl der gleichen Typen
    score = 0
    total_types = set(structure1.keys()).union(set(structure2.keys()))
    for type_name in total_types:
        if type_name in structure1 and type_name in structure2:
            score += min(len(structure1[type_name]), len(structure2[type_name]))
        elif type_name in structure1 or type_name in structure2:
            score -= 1
    
    max_score = sum(max(len(structure1.get(t, [])), len(structure2.get(t, []))) for t in total_types)
    similarity = score / max_score if max_score > 0 else 0
    return similarity


def clean_ifc(ifc_file_path, printout=False):
    """
    Clean an IFC file by creating a new IFC file that contains only one instance
    of each specified element type, preserving their attributes and property sets.

    Parameters:
    ifc_file_path (str): Path to the input IFC file.
    printout (bool): Whether to print out debug information.

    Returns:
    ifcopenshell.file: A new IFC model containing one instance of each specified element type.
    """
    try:
        # Open the IFC file
        ifc_model = ifcopenshell.open(ifc_file_path)

        # Create a new empty IFC file
        new_ifc_model = ifcopenshell.file()

        # Add the necessary header information
        for entity in ifc_model.by_type('IfcProject'):
            new_ifc_model.createIfcProject(
                entity.GlobalId, entity.OwnerHistory, entity.Name, entity.Description,
                entity.ObjectType, entity.LongName, entity.Phase
            )

        # Define the types to keep one instance of
        types_to_keep = [
            'IfcWall', 'IfcDoor', 'IfcWindow', 'IfcSlab', 'IfcColumn', 'IfcBeam',
            'IfcRoof', 'IfcStair', 'IfcRamp', 'IfcSpace', 'IfcZone', 'IfcCovering'
        ]

        # Dictionary to track added types
        added_types = {type_name: False for type_name in types_to_keep}

        for type_name in types_to_keep:
            instances = ifc_model.by_type(type_name)
            if instances:
                instance = instances[0]
                new_instance = new_ifc_model.add(instance)
                added_types[type_name] = True

                # Copy all attributes and property sets
                for attribute in instance.__dict__:
                    setattr(new_instance, attribute, getattr(instance, attribute))
                for pset in ifcopenshell.util.element.get_psets(instance):
                    ifcopenshell.util.element.add_pset(new_ifc_model, new_instance, pset)
        
        if printout:
            print(f"Cleaned IFC file created with types: {list(added_types.keys())}")
        return new_ifc_model

    except FileNotFoundError:
        print(f"File not found: {ifc_file_path}")
        return ifcopenshell.file()
    except Exception as e:
        print(f"Error cleaning IFC file: {e}")
        return ifcopenshell.file()


def get_element_types(ifc_path, printout=False):
    """
    Get a list of all element types present in an IFC file.

    Parameters:
    ifc_path (str): Path to the IFC file.
    printout (bool): Whether to print out debug information.

    Returns:
    list: A list of element types.
    """
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        element_types = set()
        for entity in ifc_file:
            element_types.add(entity.is_a())
        if printout:
            print(f"Element types: {element_types}")
        return list(element_types)
    except FileNotFoundError:
        print(f"File not found: {ifc_path}")
        return []
    except Exception as e:
        print(f"Error parsing IFC file: {e}")
        return []


def get_psets_for_entity(ifc_path, entity_type, printout=False):
    """
    Get a list of all property sets (psets) that an entity type can have in an IFC file.

    Parameters:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity type (e.g., IfcSlab, IfcWall).
    printout (bool): Whether to print out debug information.

    Returns:
    list: A list of property sets for the specified entity type.
    """
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        psets = set()
        for entity in ifc_file.by_type(entity_type):
            if hasattr(entity, 'IsDefinedBy'):
                for definition in entity.IsDefinedBy:
                    if definition.is_a('IfcRelDefinesByProperties'):
                        psets.add(definition.RelatingPropertyDefinition.Name)
        if printout:
            print(f"Psets for {entity_type}: {psets}")
        return list(psets)
    except FileNotFoundError:
        print(f"File not found: {ifc_path}")
        return []
    except Exception as e:
        print(f"Error retrieving psets for {entity_type}: {e}")
        return []


def get_properties_in_pset(ifc_path, pset_name, printout=False):
    """
    Get a list of all properties in a given property set (pset) in an IFC file.

    Parameters:
    ifc_path (str): Path to the IFC file.
    pset_name (str): Name of the property set.
    printout (bool): Whether to print out debug information.

    Returns:
    list: A list of properties in the specified property set.
    """
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        for entity in ifc_file.by_type('IfcPropertySet'):
            if entity.Name == pset_name:
                properties = [prop.Name for prop in entity.HasProperties]
                if printout:
                    print(f"Properties in {pset_name}: {properties}")
                return properties
        return []
    except FileNotFoundError:
        print(f"File not found: {ifc_path}")
        return []
    except Exception as e:
        print(f"Error retrieving properties in pset {pset_name}: {e}")
        return []


def get_property_value(ifc_path, entity_type, pset_name, property_name, printout=False):
    """
    Get the value of a specific property from a given entity type and property set in an IFC file.

    Parameters:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity type (e.g., IfcSlab, IfcWall).
    pset_name (str): Name of the property set.
    property_name (str): Name of the property.
    printout (bool): Whether to print out debug information.

    Returns:
    Any: The value of the specified property.
    """
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        for entity in ifc_file.by_type(entity_type):
            if hasattr(entity, 'IsDefinedBy'):
                for definition in entity.IsDefinedBy:
                    if definition.is_a('IfcRelDefinesByProperties'):
                        pset = definition.RelatingPropertyDefinition
                        if pset.Name == pset_name:
                            for prop in pset.HasProperties:
                                if prop.Name == property_name:
                                    if printout:
                                        print(f"Value of {property_name} in {pset_name} "
                                              f"for {entity_type}: {prop.NominalValue}")
                                    return prop.NominalValue
        raise ValueError(f"Property '{property_name}' not found in pset '{pset_name}' "
                         f"for entity type '{entity_type}'")
    except FileNotFoundError:
        print(f"File not found: {ifc_path}")
        raise ValueError(f"File not found: {ifc_path}")
    except Exception as e:
        print(f"Error retrieving property value: {e}")
        raise ValueError(f"Error retrieving property value: {e}")


def compare_ifcs(ifc_path1, ifc_path2, printout=False):
    """
    Compare two IFC files and calculate a similarity score based on the presence and values of properties.

    Parameters:
    ifc_path1 (str): Path to the first IFC file.
    ifc_path2 (str): Path to the second IFC file.
    printout (bool): Whether to print out debug information.

    Returns:
    dict: A dictionary with requests made, matches, and similarity score.
    """
    element_types = get_element_types(ifc_path1, printout)
    
    all_psets = {}
    for entity_type in element_types:
        psets = get_psets_for_entity(ifc_path1, entity_type, printout)
        all_psets[entity_type] = psets

    all_properties = {}
    for entity_type, psets in all_psets.items():
        for pset in psets:
            properties = get_properties_in_pset(ifc_path1, pset, printout)
            all_properties[(entity_type, pset)] = properties

    all_values_ifc1 = []
    for (entity_type, pset), properties in all_properties.items():
        for prop in properties:
            try:
                value = get_property_value(ifc_path1, entity_type, pset, prop, printout)
                all_values_ifc1.append(value)
            except ValueError as e:
                if printout:
                    print(e)
    
    request_count = 0
    matched_count = 0
    for (entity_type, pset), properties in all_properties.items():
        for prop in properties:
            try:
                value_ifc1 = get_property_value(ifc_path1, entity_type, pset, prop, printout)
                value_ifc2 = get_property_value(ifc_path2, entity_type, pset, prop, printout)
                request_count += 1
                if isinstance(value_ifc2, type(value_ifc1)):
                    matched_count += 1
            except ValueError:
                continue
    
    similarity_score = (matched_count / request_count) * 100 if request_count > 0 else 0
    if printout:
        print(f"Requests made: {request_count}")
        print(f"Requests matched: {matched_count}")
        print(f"Similarity score: {similarity_score:.2f}%")

    return {
        "requests_made": request_count,
        "requests_matched": matched_count,
        "similarity_score": similarity_score
    }


def main():
    ifc_file1 = 'path/to/your/first.ifc'
    ifc_file2 = 'path/to/your/second.ifc'

    model1 = load_ifc(ifc_file1)
    model2 = load_ifc(ifc_file2)

    similarity_score = compare_ifc_models(model1, model2)
    print(f"Ähnlichkeit: {similarity_score:.2f}")

    result = compare_ifcs("path/to/your1.ifc", "path/to/your2.ifc", printout=True)
    print(result)


if __name__ == "__main__":
    main()
