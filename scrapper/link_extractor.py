import config as settings
import db as database_methods
import link_scrapper
from multiprocessing import Process


if __name__ == '__main__':

    print "##################################################"
    print

    if settings.WEBDRIVER_REQUIRED:
        print "# I: [Execution] <Selenium Webdriver>"
    else:
        print "# I: [Execution] <Requests and Beautiful Soup>"
    print

    if settings.FOR_JOB and settings.FOR_RESUME:

        print "# I: [For] <Jobs and Resumes>"

        queries_jobs, total_jobs = database_methods.fetch_rows(query_for="job_queries", status_for="pending")
        queries_resumes, total_resumes = database_methods.fetch_rows(query_for="resume_queries", status_for="pending")

        if settings.MULTIPROCESS_REQUIRED:

            print "# I: [Multiprocessing] <True>"

            if settings.MULTIPROCESS_TYPE == "sequential":

                print "# I: [Type] <Sequential>"
                print "# I: [Flow] <Jobs -> Resumes>"
                print "# I: [No. of Processes] <{processes}> (For each flow)".format(processes=settings.NO_OF_PROCESSES)

                print "# I: [Total Job Queries] <{total}> (Pending)".format(total=total_jobs)
                link_scrapper.fetch_links(settings.TASKS[0], queries_jobs)
                print "# I: [Total Resume Queries] <{total}> (Pending)".format(total=total_resumes)
                link_scrapper.fetch_links(settings.TASKS[1], queries_resumes)

            else:

                print "# I: [Type] <Shared>"
                print "# I: [Flow] <Jobs and Resumes as different processes>"
                print "# I: [No. of Processes] <2>"
                print "# I: [No. of Processes] <{processes}> (For each flow)".format(processes=settings.NO_OF_PROCESSES)

                print "# I: [Total Job Queries] <{total}> (Pending)".format(total=total_jobs)
                print "# I: [Total Resume Queries] <{total}> (Pending)".format(total=total_resumes)
                job_process = Process(target=link_scrapper.fetch_links, args=(settings.TASKS[0], queries_jobs,))
                resume_process = Process(target=link_scrapper.fetch_links, args=(settings.TASKS[1], queries_resumes,))

                job_process.start()
                resume_process.start()
                job_process.join()
                resume_process.join()

        else:

            print "# I: [Multiprocessing] <False>"
            print "# I: [Flow] <Jobs -> Resumes>"

            print "# I: [Total Job Queries] <{total}> (Pending)".format(total=total_jobs)
            link_scrapper.fetch_links(settings.TASKS[0], queries_jobs)
            print "# I: [Total Resume Queries] <{total}> (Pending)".format(total=total_resumes)
            link_scrapper.fetch_links(settings.TASKS[1], queries_resumes)

    elif settings.FOR_JOB or settings.FOR_RESUME:

        if settings.FOR_JOB:

            task_for = settings.TASKS[0]
            queries, total = database_methods.fetch_rows(query_for="job_queries", status_for="pending")
            print "# I: [For] <Jobs>"

        elif settings.FOR_RESUME:

            task_for = settings.TASKS[1]
            queries, total = database_methods.fetch_rows(query_for="resume_queries", status_for="pending")
            print "# I: [For] <Resumes>"

        if settings.MULTIPROCESS_REQUIRED:

            print "# I: [Multiprocessing] <True>"
            print "# I: [No. of Processes] <{processes}>".format(processes=settings.NO_OF_PROCESSES)

        else:

            print "# I: [Multiprocessing] <False>"

        print "# I: [Total Queries] <{total}> (Pending)".format(total=total)

        link_scrapper.fetch_links(task_for, queries)

    print
    print "##################################################"



