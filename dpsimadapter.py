from models.analysis_response import AnalysisResponse  # noqa: E501
from flask import make_response
import os, traceback, sys, time
import connexion
import tempfile
from multiprocessing import Pool, Array, Queue, Manager
from enum import Enum
from glob import glob

import dpsimpy
import model_db

class TaskExecutor:
    """
        This singleton class polls the request queue and
        allocates tasks to the process pool.
    """

    _task_executor = None

    # This status list is shared between the main process
    # and the child processes.
    status_list = None
    num_procs = 1
    # TODO: We currently have a limit of 1000 runs.
    # If this is to be long running, and not just a
    # short-lived Kubernetes job, we need a circular
    # buffer or disk backing for the task details.
    max_analysis=1000

    class Status(Enum):
        not_requested_yet = 0
        requested = 1
        running = 2
        complete = 3
        error = 4

    def __init__(self):
        self.out = open(str(os.getpid()) + ".main.out", "w")
        self.err = open(str(os.getpid()) + ".main.err", "w")
        self.out.write("Starting")
        self.tasks = []
        self.manager = Manager()
        self.run_queue = self.manager.Queue()
        self.pool = Pool(processes=TaskExecutor.num_procs)
        for i in range(TaskExecutor.num_procs):
            self.pool.apply_async(TaskExecutor.wait_for_run_command, (self.run_queue,))

    def close(self):
        self.pool.close()
        self.pool.join()
        self.out.close()
        self.err.close()

    def __del__(self):
        self.close()

    def error(self, message):
        self.err.write(message)
        print(message)

    @staticmethod
    def get_task_executor():
        if TaskExecutor._task_executor is None:
            TaskExecutor.status_list = Array('I', TaskExecutor.max_analysis)
            TaskExecutor.model_list = Array('I', TaskExecutor.max_analysis)
            TaskExecutor._task_executor = TaskExecutor()
        return TaskExecutor._task_executor

    def request_analysis(self, params):
        analysis_id = len(self.tasks)
        params['analysis_id'] = analysis_id
        self.tasks.append(params)
        TaskExecutor.status_list[analysis_id] = TaskExecutor.Status.requested.value
        self.run_queue.put(self.tasks[analysis_id])
        return analysis_id

    @staticmethod
    def get_status(analysis_id):
        if TaskExecutor.max_analysis > analysis_id:
            return TaskExecutor.Status(TaskExecutor.status_list[analysis_id]).name
        else:
            self.error("No analysis found with id: " + analysis_id)
            return -1

    def get_logs(self, analysis_id):
        if analysis_id >= len(self.tasks):
            return "Analysis id not recognised: " + str(analysis_id) + os.linesep

        analysis_name = "Analysis_" + str(analysis_id)
        files = glob( "logs/" + analysis_name + "_*.log")
        files.append("logs/" + analysis_name + ".log")
        logs = ""
        for file_ in files:
            try:
                with open(file_) as f:
                    logs += os.linesep + file_ + ":" + os.linesep + os.linesep + f.read()
            except Exception as e:
                logs = "Failed to read: " + file_
                self.error("Failed to read: " + file_)
        return logs

    def get_results(self, analysis_id):
        if analysis_id >= len(self.tasks):
            return "Analysis id not recognised: " + str(analysis_id) + os.linesep

        analysis_name = "Analysis_" + str(analysis_id)
        filename = "logs/" + analysis_name + ".csv"
        logs = ""
        try:
            with open(filename) as f:
                logs += os.linesep + filename + ":" + os.linesep + os.linesep + f.read()
        except:
            self.error("Failed to read: " + filename)
        return logs

    @staticmethod
    def wait_for_run_command(queue):
        while True:
            out = open(str(os.getpid()) + ".out", "w")
            err = open(str(os.getpid()) + ".err", "w")
            msg = queue.get()
            analysis_id = msg['analysis_id']
            try:
                model_id = msg['model_id']
                name = msg['name']
                analysis_name = "Analysis_" + str(analysis_id)
                out.write("run analysis: " + str(analysis_id))
                TaskExecutor.status_list[analysis_id] = TaskExecutor.Status.running.value
                logger = dpsimpy.Logger(analysis_name)
                model = model_db.get_model(model_id)
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

                #initialise dpsimpy
                reader = dpsimpy.CIMReader("Analysis_" + str(analysis_id))
                system = reader.loadCIM(50, filenames, dpsimpy.Domain.SP, dpsimpy.PhaseType.Single)
                sim = dpsimpy.Simulation("Analysis_" + str(analysis_id))
                sim.set_system(system)
                sim.set_domain(dpsimpy.Domain.SP)
                sim.set_solver(dpsimpy.Solver.NRP)
                for node in system.nodes:
                    logger.log_attribute(node.name()+'.V', 'v', node);
                sim.add_logger(logger)
                sim.run()

                # clean up the files that we created
                for tempname in filenames:
                    os.unlink(tempname)

                TaskExecutor.status_list[analysis_id] = TaskExecutor.Status.complete.value

            except Exception as e:
                TaskExecutor.status_list[analysis_id] = TaskExecutor.Status.error.value
                err.write("analysis failed: " + str(analysis_id) + " with: " + str(e))
            finally:
                err.close()
                out.close()

def add_analysis():  # noqa: E501
    """Add a new analysis
     # noqa: E501
    :rtype: AnalysisResponse
    """
    model_id = connexion.request.json['modelid']
    name = connexion.request.json['name']
    analysis_id = TaskExecutor.get_task_executor().request_analysis({ "model_id": model_id, "name": name })
    connexion.request.json['analysis_id'] = analysis_id
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
    """Get specific analysis status

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    status = TaskExecutor.get_task_executor().get_status(id_)
    return { "status": status, "id": id_ }

def get_analysis_results(id_):  # noqa: E501
    """Get specific analysis status and results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    taskExecutor = TaskExecutor.get_task_executor()
    response = make_response(taskExecutor.get_results(id_))
    response.mimetype = "text/plain"
    return response

def get_analysis_logs(id_):  # noqa: E501
    """Get specific analysis status and results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    taskExecutor = TaskExecutor.get_task_executor()
    response = make_response(taskExecutor.get_logs(id_))
    response.mimetype = "text/plain"
    return response
