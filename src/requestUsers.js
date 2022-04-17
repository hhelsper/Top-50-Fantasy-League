import _ from 'lodash';

export const requestUsers = _.memoize(async search => {
    const res = await fetch(`/get_users?search=${search}`)
    if (res.status !== 200) return [];

    const users = await res.json();
    return users;
});