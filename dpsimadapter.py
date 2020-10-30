from models.analysis_response import AnalysisResponse  # noqa: E501
import os
import dpsimpy
import connexion
import db
import tempfile


def add_analysis():  # noqa: E501
    """Add a new analysis
     # noqa: E501
    :rtype: AnalysisResponse
    """
    model_id = connexion.request.json['modelid']
    name = connexion.request.json['name']
    print("Adding analysis with name: ", name)
    logger = dpsimpy.Logger(name)
    model = db.get_model(model_id)
    files = model.files

    # prepare the files for dpsim to read. we should make dpsim accept data blobs.
    # however, that requires work in 3 projects and a technical discussion first.
    filenames = []
    for filedata in model.files:
        fp, path = tempfile.mkstemp(suffix=".xml", prefix=None, dir=None, text=True)
        filedata.seek(0)
        data = filedata.read()
        os.write(fp, data);
        os.close(fp);
        filenames.append(path)

    #initialie dpsimpy
    reader = dpsimpy.CIMReader(name)
    system = reader.loadCIM(50, filenames, dpsimpy.Domain.SP, dpsimpy.PhaseType.Single)
    sim = dpsimpy.Simulation(name)
    sim.set_system(system)
    sim.set_domain(dpsimpy.Domain.SP)
    sim.set_solver(dpsimpy.Solver.NRP)
    for node in system.nodes:
        logger.log_attribute(node.name()+'.V', 'v', node);
    sim.add_logger(logger)
    sim.run()

    # clean up the files that we created
    for name in filenames:
        os.unlink(name)

    return connexion.request.json

def delete_analysis(id_):  # noqa: E501
    """Delete specific analysis including results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    raise Exception('Unimplemented')


def get_all_analysis():  # noqa: E501
    """Get all network models

     # noqa: E501


    :rtype: List[AnalysisResponse]
    """
    raise Exception('Unimplemented')


def get_analysis(id_):  # noqa: E501
    """Get specific analysis status and results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    raise Exception('Unimplemented')
