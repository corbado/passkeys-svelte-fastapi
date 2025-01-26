<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import userStore from '../stores/user.svelte';
	import Corbado from '@corbado/web-js';

	function isRouteActive(route: string) {
		return page.url.pathname === route;
	}

	function onLogout() {
		userStore.onCorbadoLoaded(() => Corbado.logout());
		goto('/');
	}
</script>

<div>
	<nav>
		<a href="/" class="nav-logo">
			<img src="/logo.svg" alt="Corbado Logo" height="40" width="40" />
			<p>Corbado Example</p>
		</a>
		<ul>
			<li>
				<a href="/" data-selected={isRouteActive('/')}>Home</a>
			</li>
			<li>
				<a href="/userarea" data-selected={isRouteActive('/userarea')}
					>User area</a
				>
			</li>
			{#if userStore.userInfo.status === 'authenticated'}
				<li>
					<a href="/profile" data-selected={isRouteActive('/profile')}
						>Profile</a
					>
				</li>
			{:else}
				<li>
					<a href="/signup" data-selected={isRouteActive('/signup')}
						>Sign up</a
					>
				</li>
				<li>
					<a href="/login" data-selected={isRouteActive('/login')}
						>Login</a
					>
				</li>
			{/if}
		</ul>
		{#if userStore.userInfo.status === 'authenticated'}
			<button onclick={onLogout} class="button">Logout</button>
		{/if}
	</nav>
</div>
