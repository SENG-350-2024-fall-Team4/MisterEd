<template>
    <sidebar-menu :menu="menu" :hideToggle="true" />
</template>

<!-- This menu is based off of the example at https://yaminncco.github.io/vue-sidebar-menu/#/basic-usage,
    with modifications to omit icons, make unlinked dropdowns, and keep the sidebar visible at all times.
    Requires vue-sidebar-menu to be installed with `npm i vue-sidebar-menu --save`.
    TODO:
        Apply sidebar as a standalone component added to other pages
        Update page links to match the other pages in the site
        Add more visual flair (e.g. colouring, larger font in header)
        Show or hide components depending on user type
 -->

<script>
    export default {
        name: 'HelloWorld',
        data() {
            return {
                menu: [
                    {
                        header: 'Mister Ed',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/todo1',
                        title: 'Create Appoinment',
                    },
                    {
                        href: '/todo2',
                        title: 'Manage Appointments',
                    },
                    {
                        href: '/todo3',
                        title: 'Manage Profile',
                    },
                    {
                        title: 'Medical Employee Options',
                        child: [
                            {
                                href: '/todo-med/todo1',
                                title: 'Review Triages'
                            },
                            {
                                href: '/todo-med/todo2',
                                title: 'View Queued Patients'
                            },
                            {
                                href: '/todo-med/todo3',
                                title: 'Search Patients'
                            },
                            {
                                href: '/todo-med/todo4',
                                title: 'ED Dashboard'
                            }
                        ]
                    },
                    {
                        title: 'Admin Options',
                        child: [
                            {
                                href: '/todo-admin/todo1',
                                title: 'Manage Facilities'
                            },
                            {
                                href: '/todo-admin/todo2',
                                title: 'Manage Staff'
                            },
                            {
                                href: '/todo-admin/todo3',
                                title: 'Edit Site Banner'
                            }
                        ]
                    }
                ]
            }
        }
    }
</script>
