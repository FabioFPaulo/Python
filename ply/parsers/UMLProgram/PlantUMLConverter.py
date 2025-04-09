class PlantUMLConverter:
    # Dictionaries to store actors and nodes using their alias as keys
    # Example: actors = { "Alice": "A user" }
    actors = {}

    nodes = {}

    # List of tuples storing relationships (mode, alias1, alias2)
    # Example: links = [("Association", "Alice", "System")]
    links = []

    # Parsed input content from the parser
    parsed_contents = None

    def __init__(self, parsed_contents):
        self.parsed_contents = parsed_contents
        self._run()  # Process parsed contents and populate actors, nodes, and links

    def update_contents(self, parsed_contents):
        """Update parsed contents and regenerate the UML structure."""

        self.parsed_contents = parsed_contents
        self._run()

    def build_uml(self) -> str:
        """Construct the final PlantUML string output."""
        uml = ""

        # Define actors in PlantUML format
        for alias, label in self.actors.items():
            uml += f"actor \"{label}\" as {alias} \n"

        # Define nodes inside a rectangle (a container)
        uml += "rectangle {\n"
        for alias, label in self.nodes.items():
            uml += f"\t\"{label}\" as ({alias}) \n"

        # Define the links between actors and/or nodes
        for link in self.links:
            mode, alias1, alias2 = link

            # Get UML arrow style and label based on mode
            row, linkLabel = self._getUMLArrowLabel(mode)

            # Wrap non-actors in parentheses to match UML syntax
            alias1 = alias1 if self._aliasLinkType(
                alias1) == "ACTOR" else f"({alias1})"
            alias2 = alias2 if self._aliasLinkType(
                alias2) == "ACTOR" else f"({alias2})"

            # Add optional label to the link
            linkLabel = f": {linkLabel}" if linkLabel else ""

            uml += f"\t {alias1} {row} {alias2} {linkLabel}\n"

        uml += "}\n"

        # Wrap the diagram in PlantUML boilerplate
        return f"""
========================================================
================PlantUML Code Generator ================
========================================================
@startuml top_to_bottom
skinparam packageStyle rectangle
left to right direction

{uml}
@enduml
========================================================
"""

    def _existsActor(self, actor: str):
        """Check if an actor exists"""

        return actor in self.actors.keys()

    def _existsNode(self, nodeAlias: str):
        """Check if a node exists"""

        return nodeAlias in self.nodes.keys()

    def _aliasLinkType(self, aliasLink: str):
        """Determine if an alias refers to an ACTOR or NODE"""

        if (aliasLink in self.actors.keys()):
            return "ACTOR"
        elif aliasLink in self.nodes.keys():
            return "NODE"
        raise Exception(f"Undefined alias link type {aliasLink}")

    def _getUMLArrowLabel(self, mode: str):
        """Return UML arrow style and label for each relationship type"""

        if (mode == "Association"):
            return ("--", None)
        elif mode == "Include":
            return ("..>", "<<include>>")
        elif mode == "Extend":
            return ("<..", "<<extend>>")
        elif mode == "Inh":
            return ("<|-", None)
        else:
            raise Exception(f"[_getUMLROW] Invalid mode {mode}")

    def _run(self):
        """Parse the provided content and populate actors, nodes, and links."""

        if (self.parsed_contents == None):
            raise Exception("Content not supported")

        for stmt in self.parsed_contents:
            # stmt is a tuple like: (MODE, ALIAS, STRING)
            mode, alias, label = (stmt[0], stmt[1], stmt[2])

            if (mode == "Actor"):
                self.actors[alias] = label
            elif mode == "Node":
                self.nodes[alias] = label
            elif mode in ("Association", "Include", "Extend", "Inh"):
                # Ensure both aliases in the link exist
                if not (alias in self.actors.keys() or alias in self.nodes.keys()):
                    raise Exception(f"{stmt}:\t Alias {alias} not exists")

                if not (label in self.actors.keys() or label in self.nodes.keys()):
                    raise Exception(f"{stmt}:\t Alias {label} not exists")

                # Add to links list
                self.links.append((mode, alias, label))

    def __str__(self):
        """Return a string summary of the current internal state."""

        return f"Actors:\t{len(self.actors.keys())}\nNodes:\t{len(self.nodes.keys())}\nLinks:\t{len(self.links)}"
